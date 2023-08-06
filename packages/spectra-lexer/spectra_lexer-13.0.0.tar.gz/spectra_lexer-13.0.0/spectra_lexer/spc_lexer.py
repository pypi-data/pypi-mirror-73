from collections import defaultdict
from typing import Iterable, List, Mapping

from spectra_lexer.lexer import LexerRule
from spectra_lexer.lexer.composite import PriorityRuleMatcher
from spectra_lexer.lexer.exact import StrokeMatcher, WordMatcher
from spectra_lexer.lexer.lexer import LexerResult, StenoLexer
from spectra_lexer.lexer.parallel import ParallelMapper
from spectra_lexer.lexer.prefix import UnorderedPrefixMatcher
from spectra_lexer.lexer.special import DelimiterMatcher, SpecialMatcher
from spectra_lexer.resource.keys import StenoKeyLayout
from spectra_lexer.resource.rules import StenoRule
from spectra_lexer.resource.translations import ExamplesDict, RuleID, Translation

TranslationPairs = Iterable[Translation]  # Iterable collection of steno translations.


class TranslationFilter:
    """ Size-based filter for RTFCRE steno translations. """

    # Cutoffs for translation filters based on their size.
    SIZE_MINIMUM = 1   # Below this size, the filter blocks everything.
    SIZE_SMALL = 10
    SIZE_MEDIUM = 12
    SIZE_LARGE = 15
    SIZE_MAXIMUM = 20  # At this size and above, the filter is disabled.
    # Ordered list of all filter sizes for GUI display.
    SIZES = [SIZE_MINIMUM, SIZE_SMALL, SIZE_MEDIUM, SIZE_LARGE, SIZE_MAXIMUM]

    def __init__(self, size:int) -> None:
        self._size = size

    def filter(self, translations:TranslationPairs) -> TranslationPairs:
        """ Return only translations where every string is below the maximum size. """
        size = self._size
        if size < self.SIZE_MINIMUM:
            # If the size is below minimum, it could be a dummy run. Keep nothing.
            return []
        elif size >= self.SIZE_MAXIMUM:
            # If the size is maximum, filtering is unnecessary. Keep everything.
            return translations
        else:
            # Eliminate long translations depending on the size factor.
            return [(keys, letters) for keys, letters in translations
                    if len(keys) <= size and len(letters) <= size]


class StenoAnalyzer:
    """ Key-converting wrapper for the lexer. Also uses multiprocessing to make an examples index. """

    def __init__(self, keymap:StenoKeyLayout, lexer:StenoLexer, rule_sep:StenoRule,
                 refmap:Mapping[LexerRule, StenoRule], idmap:Mapping[LexerRule, RuleID]) -> None:
        self._to_skeys = keymap.rtfcre_to_skeys   # Converts user RTFCRE steno strings to s-keys.
        self._to_rtfcre = keymap.skeys_to_rtfcre  # Converts s-keys back to RTFCRE.
        self._lexer = lexer                       # Main analysis engine; operates only on s-keys.
        self._rule_sep = rule_sep                 # Stroke separator rule.
        self._refmap = refmap                     # Mapping of lexer rule objects to their original StenoRules.
        self._idmap = idmap                       # Mapping of lexer rule objects to valid example rule IDs.

    @staticmethod
    def _result_info(result:LexerResult) -> str:
        """ Return an info string for this result. The output is nowhere near reliable if some keys are unmatched. """
        if not result.unmatched_skeys:
            info = "Found complete match."
        elif result.rules:
            info = "Incomplete match. Not reliable."
        else:
            info = "No matches found."
        return info

    def query(self, keys:str, letters:str, *, strict_mode=False) -> StenoRule:
        """ Return a lexer analysis matching <keys> to <letters> in standard steno rule format.
            If <strict_mode> is True and the best result is missing keys, return a fully unmatched result instead. """
        skeys = self._to_skeys(keys)
        result = self._lexer.query(skeys, letters)
        keys = self._to_rtfcre(skeys)
        info = self._result_info(result)
        rule = StenoRule(keys, letters, info)
        unmatched_skeys = result.unmatched_skeys
        if strict_mode and unmatched_skeys:
            unmatched_skeys = skeys
        else:
            for lr, start in zip(result.rules, result.rule_positions):
                child = self._refmap[lr]
                length = len(lr.letters)
                rule.add_connection(child, start, length)
        if unmatched_skeys:
            unmatched_keys = self._to_rtfcre(unmatched_skeys)
            rule.add_unmatched(unmatched_keys)
        return rule

    def compound_query(self, translations:TranslationPairs, **kwargs) -> StenoRule:
        """ Return a compound lexer analysis of several translations joined together. """
        rules = [self.query(keys, letters, **kwargs) for keys, letters in translations]
        n = len(rules)
        if not n:
            raise ValueError("Need at least 1 translation, got 0.")
        if n == 1:
            return rules[0]
        delimited_seq = [self._rule_sep] * (2 * n - 1)
        delimited_seq[::2] = rules
        return StenoRule.join(delimited_seq)

    def best_translation(self, keys_iter:Iterable[str], letters:str) -> str:
        """ Return the best (most accurate) match to <letters> out of <keys_iter> according to lexer ranking. """
        keys_list = list(keys_iter)
        if not keys_list:
            raise ValueError("Cannot find the best of 0 translations.")
        if len(keys_list) == 1:
            best_index = 0
        else:
            skeys_list = [self._to_skeys(keys) for keys in keys_list]
            best_index = self._lexer.best_translation(skeys_list, letters)
        return keys_list[best_index]

    def _query_rule_ids(self, keys:str, letters:str) -> List[str]:
        """ Make a parallel-safe lexer query and return the result as a list of strings.
            Results may be returned out of order, so the output starts with the original keys and letters.
            The identities of rule objects do not survive pickling, so only ID strings are returned.
            Only complete matches should return rule IDs. Rule positions are discarded. """
        skeys = self._to_skeys(keys)
        result = self._lexer.query(skeys, letters)
        output = [keys, letters]
        if not result.unmatched_skeys:
            for lr in result.rules:
                if lr in self._idmap:
                    output.append(self._idmap[lr])
        return output

    def compile_index(self, translations:TranslationPairs, *, size:int=None, process_count=0) -> ExamplesDict:
        """ Run the lexer on all given <translations> with an optional <size> filter.
            This is a big job; do it in parallel if possible using <process_count> processes at once.
            Then make a index containing each rule's ID mapped to a dict of every translation that used it. """
        mapper = ParallelMapper(self._query_rule_ids, process_count=process_count)
        if size is not None:
            translations = TranslationFilter(size).filter(translations)
        results = mapper.starmap(translations)
        index = defaultdict(dict)
        for keys, letters, *rule_ids in results:
            for r_id in rule_ids:
                index[r_id][keys] = letters
        return index

    def normalize_keys(self, keys:str) -> str:
        """ Normalize a set of RTFCRE keys by converting back and forth. """
        skeys = self._to_skeys(keys)
        return self._to_rtfcre(skeys)


def build_analyzer(keymap:StenoKeyLayout, rules:Iterable[StenoRule]) -> StenoAnalyzer:
    """ Distribute rules and build the rule matchers, lexer and analyzer. """
    refmap = {}
    matcher_groups = []
    key_sep = keymap.separator_key()
    key_special = keymap.special_key()

    # Separators are force-matched before the normal matchers can waste cycles on them.
    sep_matcher = DelimiterMatcher()
    lr_sep = LexerRule(key_sep, "", 0)
    rule_sep = StenoRule(key_sep, "", "stroke separator")
    refmap[lr_sep] = rule_sep
    sep_matcher.add(lr_sep)
    matcher_groups.append([sep_matcher])

    # Matchers for rules without special behavior are processed as one group.
    prefix_matcher = UnorderedPrefixMatcher(key_sep, key_special)
    stroke_matcher = StrokeMatcher(key_sep)
    word_matcher = WordMatcher()
    idmap = {}
    for rule in rules:
        # Convert each rule to lexer format. Rule weight is assigned based on letters matched.
        # Rare rules are uncommon in usage and/or prone to causing false positives.
        # They have slightly reduced weight so that other rules with equal letter count are chosen first.
        # Word rules may be otherwise equal to some prefixes and suffixes; they need *more* weight to win.
        skeys = keymap.rtfcre_to_skeys(rule.keys)
        letters = rule.letters
        weight = 10 * len(letters) - rule.is_rare + rule.is_word
        lr = LexerRule(skeys, letters, weight)
        # Map every lexer-format rule to the original so we can convert back.
        refmap[lr] = rule
        # Rules without special behavior should be in example indices.
        idmap[lr] = rule.id
        # Add the lexer rule to one of the rule matchers based on flags.
        if rule.is_reference:
            # Reference-only rules are not matched directly.
            pass
        elif rule.is_stroke:
            # Stroke rules are matched only by complete strokes.
            stroke_matcher.add(lr)
        elif rule.is_word:
            # Word rules are matched only by whole words (but still case-insensitive).
            word_matcher.add(lr)
        else:
            # All other rules are added to the tree-based prefix matcher.
            prefix_matcher.add(lr)
    matcher_groups.append([prefix_matcher, stroke_matcher, word_matcher])

    # Use the special matcher only if absolutely nothing else has worked.
    special_matcher = SpecialMatcher(key_sep)
    for pred in SpecialMatcher.Predicate.LIST:
        # Rules with special behavior must be handled case-by-case.
        lr = LexerRule(key_special, "", 0)
        info = key_special + ": " + pred.desc
        rule = StenoRule(key_special, "", info, set(), "", pred.repl)
        refmap[lr] = rule
        special_matcher.add_test(lr, pred)
    matcher_groups.append([special_matcher])

    # Each matcher group is tried in order of priority (separators first, specials last).
    matcher = PriorityRuleMatcher(*matcher_groups)
    lexer = StenoLexer(matcher)
    return StenoAnalyzer(keymap, lexer, rule_sep, refmap, idmap)
