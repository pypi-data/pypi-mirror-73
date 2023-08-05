import re
import collections
import string


def getSimilarity(nlp, maxDialogue, minDialogue, start, end):
    maxWordSnippet = (
        " ".join(re.split("(?:,\s)|[, ]", maxDialogue))[start : end + 1]
        if end
        else " ".join(re.split("(?:,\s)|[, ]", maxDialogue)[start:])
    )
    minWordSnippet = " ".join(re.split("(?:,\s)|[, ]", minDialogue))

    subtitleNLP = nlp(maxWordSnippet)
    scriptNLP = nlp(minWordSnippet)

    if not subtitleNLP.vector_norm or not scriptNLP.vector_norm:
        return 0
    similarity = subtitleNLP.similarity(scriptNLP)
    return similarity


def isGoodEnough(nlp, scriptContent, subsContent, subsWord, scriptPercent, subsPercent):
    def getNumberOfSameWords(scriptContent, subsContent):
        count = 0
        for scriptLemma in set(scriptContent["lemma"]):
            for subtitleLemma in set(subsContent["lemma"]):
                if scriptLemma == subtitleLemma:
                    count += 1
        return count

    # number of words in subtitle and screenplay dialogue that's the same
    count = getNumberOfSameWords(subsContent, scriptContent)

    # minimum dialogue length between script line and subtitle
    minDialogue = subsContent
    maxDialogue = scriptContent
    if len(scriptContent["lemma"]) < len(subsContent["lemma"]):
        minDialogue = scriptContent
        maxDialogue = subsContent

    def getMaxSimilarity(word):
        index = 0
        maxSimilarity = 0
        maxIndex = 0

        if len(minDialogue["dialogue"]) >= len(maxDialogue["dialogue"]):
            maxSimilarity = getSimilarity(
                nlp, maxDialogue["dialogue"], minDialogue["dialogue"], index, None,
            )
            maxIndex = index
        else:
            # split dialogue by whitespace, and remove remaining punctuations
            maxDialogueTokens = (
                maxDialogue["dialogue"]
                .translate(str.maketrans("", "", string.punctuation))
                .split()
            )

            minDialogueTokens = (
                minDialogue["dialogue"]
                .translate(str.maketrans("", "", string.punctuation))
                .split()
            )

            while index + len(minDialogue["dialogue"]) < len(maxDialogue["dialogue"]):
                if word in maxDialogueTokens[index : index + len(minDialogueTokens)]:
                    similarity = getSimilarity(
                        nlp,
                        maxDialogue["dialogue"],
                        minDialogue["dialogue"],
                        index,
                        index + len(minDialogue["dialogue"]),
                    )
                    if similarity > maxSimilarity:
                        maxSimilarity = similarity
                        maxIndex = index
                index += 1

        maxSimilarity = round(maxSimilarity, 3)
        if maxSimilarity >= 1 and len(minDialogue["dialogue"]) != len(
            maxDialogue["dialogue"]
        ):
            maxSimilarity = 0.99
        return (maxSimilarity, maxIndex)

    if len(minDialogue["lemma"]) == len(maxDialogue["lemma"]) and collections.Counter(
        minDialogue["lemma"]
    ) == collections.Counter(maxDialogue["lemma"]):
        maxSimilarity = 0.99
        maxIndex = 0
    else:
        maxSimilarity, maxIndex = getMaxSimilarity(subsWord)

    goodEnoughPercent = abs(scriptPercent - subsPercent) <= 0.15

    return (
        (count >= 5 or (goodEnoughPercent and maxSimilarity >= 0.85)),
        maxSimilarity,
        maxIndex,
    )


def getMatchingDistinctWords(
    nlp, scriptUnique, subsUnique, script, subs, previousMatches
):
    """
    - traverses subsUnique and scriptUnique until there's a matching unique word.
    - if similar enough, push to matchUniqueWords
    - else, remove
    """
    matchingUniqueWords = previousMatches

    for subsWord, subsValue in subsUnique.items():
        for scriptWord, scriptValue in scriptUnique.items():
            if subsWord == scriptWord:
                takenScript = {}
                takenSubs = {}

                for sceneNumber, scriptInstances in scriptValue.items():
                    for scriptIndex, scriptContent in enumerate(
                        scriptInstances["content"]
                    ):
                        scriptPercent = scriptContent["index"] / len(script)

                        for subsIndex, subsContent in enumerate(subsValue["content"]):
                            subsPercent = subsContent["timestamp"][0] / (
                                subs[-1]["start"].seconds - subs[0]["start"].seconds
                            )

                            goodEnough, maxSimilarity, maxIndex = isGoodEnough(
                                nlp,
                                scriptContent,
                                subsContent,
                                subsWord,
                                scriptPercent,
                                subsPercent,
                            )

                            # if match already made for current subtitle OR current script, then
                            # don't bother considering current script<->subtitle match
                            existingTakenSubsBetter = (
                                subsIndex in takenSubs
                                and takenSubs[subsIndex]["similarity"] >= maxSimilarity
                            )

                            existingTakenScriptsFromSubsBetter = (
                                subsIndex in takenSubs
                                and (
                                    takenScript[takenSubs[subsIndex]["script"]][
                                        "similarity"
                                    ]
                                    >= maxSimilarity
                                )
                            )

                            existingTakenScriptsBetter = (
                                scriptIndex in takenScript
                                and takenScript[scriptIndex]["similarity"]
                                >= maxSimilarity
                            )

                            existingTakenSubsFromScriptsBetter = (
                                scriptIndex in takenScript
                                and (
                                    takenSubs[takenScript[scriptIndex]["subs"]][
                                        "similarity"
                                    ]
                                    >= maxSimilarity
                                )
                            )

                            if (
                                existingTakenSubsBetter
                                and existingTakenScriptsFromSubsBetter
                            ):
                                continue

                            if (
                                existingTakenScriptsBetter
                                and existingTakenSubsFromScriptsBetter
                            ):
                                continue

                            if (
                                scriptIndex in takenScript
                                and not existingTakenSubsFromScriptsBetter
                            ):
                                del takenSubs[takenScript[scriptIndex]["subs"]]
                                del takenScript[scriptIndex]

                            if (
                                subsIndex in takenSubs
                                and not existingTakenScriptsFromSubsBetter
                            ):
                                del takenScript[takenSubs[subsIndex]["script"]]
                                del takenSubs[subsIndex]

                            if goodEnough:
                                takenSubs[subsIndex] = {
                                    "percent": subsPercent,
                                    "similarity": maxSimilarity,
                                    "script": scriptIndex,
                                }
                                takenScript[scriptIndex] = {
                                    "percent": scriptPercent,
                                    "similarity": maxSimilarity,
                                    "subs": subsIndex,
                                    "scene": sceneNumber,
                                }

                for part in takenScript.items():
                    sceneNumber = part[1]["scene"]
                    if (
                        sceneNumber not in matchingUniqueWords
                        or subsWord not in matchingUniqueWords[sceneNumber]
                    ):
                        matchingUniqueWords.setdefault(sceneNumber, {})
                        matchingUniqueWords[sceneNumber][subsWord] = [
                            {
                                "timestamp": subsValue["content"][part[1]["subs"]][
                                    "timestamp"
                                ],
                                "index": scriptValue[sceneNumber]["content"][part[0]][
                                    "index"
                                ],
                                "sceneNumber": sceneNumber,
                                "subsDialogue": subsValue["content"][part[1]["subs"]][
                                    "dialogue"
                                ],
                            }
                        ]
                    else:
                        matchingUniqueWords[sceneNumber][subsWord].append(
                            {
                                "timestamp": subsValue["content"][part[1]["subs"]][
                                    "timestamp"
                                ],
                                "index": scriptValue[sceneNumber]["content"][part[0]][
                                    "index"
                                ],
                                "scene": sceneNumber,
                                "subsDialogue": subsValue["content"][part[1]["subs"]][
                                    "dialogue"
                                ],
                            }
                        )

    # remove false positives
    # matchingUniqueWords is sorted
    for sceneNumber, sceneWords in matchingUniqueWords.items():
        prevMatch = {}
        prevPrevMatch = {}
        for word, wordInstances in sceneWords.items():
            if (
                "timestamp" in prevMatch
                and wordInstances["timestamp"] < prevMatch["timestamp"]
            ):
                if (
                    "timestamp" in prevPrevMatch
                    and prevPrevMatch["timestamp"] < wordInstances["timestamp"]
                ):
                    del prevMatch
                else:
                    del wordInstances
            prevPrevMatch = prevMatch
            prevMatch = wordInstances

    return matchingUniqueWords
