import re
import json

from subtitle_sync.utils.traverseDialogue import traverseDialogue
from subtitle_sync.utils.extractLemmas import (
    extractLemmaScript,
    extractLemmaSubs,
)
from subtitle_sync.utils.getMatchingDistinctWords import getMatchingDistinctWords


def getUniqueWordsSubs(subsLemma):
    uniqueWords = {}
    for subtitle in subsLemma:
        for lemmaWord in subtitle["lemma"]:
            if len(lemmaWord) <= 2:
                continue
            if (
                lemmaWord in uniqueWords
                and "content" in uniqueWords[lemmaWord]
                and len(uniqueWords[lemmaWord]["content"])
                and uniqueWords[lemmaWord]["content"][-1]["dialogue"]
                == subtitle["content"]
            ):
                continue
            uniqueWords.setdefault(
                lemmaWord, {"count": 0, "content": []},
            )
            uniqueWords[lemmaWord]["count"] += 1
            uniqueWords[lemmaWord]["content"].append(
                {
                    "lemma": subtitle["lemma"],
                    "dialogue": subtitle["content"],
                    "timestamp": (subtitle["start"], subtitle["end"]),
                }
            )
    subsCountOfOne = {}
    subsCountOfTwo = {}
    subsCountOfThree = {}
    for k, v in uniqueWords.items():
        if v["count"] == 1:
            subsCountOfOne[k] = v
        elif v["count"] == 2:
            subsCountOfTwo[k] = v
        elif v["count"] == 3:
            subsCountOfThree[k] = v

    return [subsCountOfOne, subsCountOfTwo, subsCountOfThree]


def getUniqueWordsScript(scriptLemma):
    uniqueWords = {}
    for index, section in enumerate(scriptLemma):
        for lemmaWord in section["lemma"]:
            if len(lemmaWord) <= 2:
                continue
            if (
                lemmaWord in uniqueWords
                and "scenes" in uniqueWords[lemmaWord]
                and len(uniqueWords[lemmaWord]["scenes"])
                and section["sceneNumber"] in uniqueWords[lemmaWord]["scenes"]
            ):
                x = filter(
                    lambda y: y["index"] == index,
                    uniqueWords[lemmaWord]["scenes"][section["sceneNumber"]]["content"],
                )
                if len(list(x)):
                    continue
            uniqueWords.setdefault(lemmaWord, {"count": 0, "scenes": {}})
            uniqueWords[lemmaWord]["scenes"].setdefault(
                section["sceneNumber"], {"content": []}
            )
            uniqueWords[lemmaWord]["count"] += 1
            uniqueWords[lemmaWord]["scenes"][section["sceneNumber"]]["content"].append(
                {
                    "lemma": section["lemma"],
                    "dialogue": section["dialogue"],
                    "index": index,
                }
            )

    scriptCountOfOne = {}
    scriptCountOfTwo = {}
    scriptCountOfThree = {}
    for k, v in uniqueWords.items():
        if k == "army":
            dfsdf = 0
        if v["count"] == 1:
            scriptCountOfOne.setdefault(k, {})
            scriptCountOfOne[k] = v["scenes"]
        elif v["count"] == 2:
            scriptCountOfTwo.setdefault(k, {})
            scriptCountOfTwo[k] = v["scenes"]
        elif v["count"] == 3:
            scriptCountOfThree.setdefault(k, {})
            scriptCountOfThree[k] = v["scenes"]

    return [scriptCountOfOne, scriptCountOfTwo, scriptCountOfThree]


def getDistinctWordsTimestampScript(script, matchingDistinct):
    for sceneNumber, sceneContent in matchingDistinct.items():
        for matchingWord, matchingWordInstance in sceneContent.items():
            for content in matchingWordInstance:
                if (
                    "timestamp" in script[content["index"]]
                    and max(
                        script[content["index"]]["timestamp"][0],
                        content["timestamp"][0],
                    )
                    - min(
                        script[content["index"]]["timestamp"][1],
                        content["timestamp"][1],
                    )
                    < 20
                ):
                    startTime = min(
                        script[content["index"]]["timestamp"][0],
                        content["timestamp"][0],
                    )
                    endTime = max(
                        script[content["index"]]["timestamp"][1],
                        content["timestamp"][1],
                    )
                    script[content["index"]]["timestamp"] = [startTime, endTime]
                    script[content["index"]]["scene_number"] = sceneNumber
                else:
                    script[content["index"]]["timestamp"] = content["timestamp"]
                    script[content["index"]]["scene_number"] = sceneNumber
                script[content["index"]]["distinct"] = content
    return script


def getDistinctWordsTimestampSubs(subsLemma, subsUnique):
    for subtitle in subsLemma:
        for word in subtitle["lemma"]:
            if word in subsUnique:
                if "distinct" in subtitle:
                    subtitle["distinct"].append(word)
                else:
                    subtitle["distinct"] = [word]
    return subsLemma


def markScriptWithRareWordsTimestamp(nlp, script, subs):
    """
    1. remove stopwords from subtitles, then get unique words from them. same thing for script
    3. get word matches of unique script/sub words. separate matches with count of  1, 2, and 3
    4. tag timestamps of unique words into the script
    """

    subsLemma = extractLemmaSubs(nlp, subs)
    scriptLemma = extractLemmaScript(nlp, script)

    subsUnique = getUniqueWordsSubs(subsLemma)
    scriptUnique = getUniqueWordsScript(scriptLemma)

    matchingDistinct = getMatchingDistinctWords(
        nlp, scriptUnique[0], subsUnique[0], script, subs, {}
    )
    matchingDistinct = getMatchingDistinctWords(
        nlp, scriptUnique[1], subsUnique[1], script, subs, matchingDistinct
    )
    matchingDistinct = getMatchingDistinctWords(
        nlp, scriptUnique[2], subsUnique[2], script, subs, matchingDistinct
    )

    scriptUniqueTimestamp = getDistinctWordsTimestampScript(
        scriptLemma, matchingDistinct
    )
    # subsUniqueTimestamp = getDistinctWordsTimestampSubs(subsLemma, subsUnique)

    file0 = open("subHelp.json", "w+")
    json.dump(subsUnique, file0, indent=4)

    file0 = open("scriptLemma.json", "w+")
    json.dump(scriptLemma, file0, indent=4)

    file0 = open("scriptHelp.json", "w+")
    json.dump(scriptUnique, file0, indent=4)

    file0 = open("matchingHelp.json", "w+")
    json.dump(matchingDistinct, file0, indent=4)

    file0 = open("test.json", "w+")
    json.dump(scriptUniqueTimestamp, file0, indent=4)

    return (
        script,
        scriptUniqueTimestamp,
        # subsUniqueTimestamp
    )
