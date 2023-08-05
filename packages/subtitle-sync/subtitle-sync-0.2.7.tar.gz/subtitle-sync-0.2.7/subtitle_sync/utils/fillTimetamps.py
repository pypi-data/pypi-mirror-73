import copy


# final is the number of divisions of the scene. when curr == final, scene is finished
def getScenesToBeTagged(scriptWithTimestamp):
    scenesToBeTagged = {}

    for page in scriptWithTimestamp:
        for content in page["content"]:
            if "scene_info" in content:
                scenesToBeTagged[content["scene_number"]] = True
    return scenesToBeTagged


def isCountCondition(scene):
    return scene["type"] != "ACTION" or (
        len(scene["content"]) > 1
        or (
            len(scene["content"]) == 1
            and "CONTINUED" not in scene["content"][0]["text"]
        )
    )


def isTransition(scene):
    return scene["type"] == "TRANSITION" and "CONTINUED" not in scene["content"]["text"]


# get the next scene after current scene
def getNextScene(scriptWithTimestamp, currTagScenes, latestTimestamp):
    minTime = None
    currSceneIsMin = False
    minSceneGroup = None
    minSceneNumber = 0
    currSceneNumber = 0
    GOOD_ENOUGH_DIFFERENCE = 20
    sceneGroup = []
    sceneHasGoodEnoughDifference = False

    for page in scriptWithTimestamp:
        for content in page["content"]:
            if (
                "scene_info" in content
                and currTagScenes[content["scene_number"]] == True
            ):
                for scene in content["scene"]:
                    if currSceneNumber != content["scene_number"]:
                        if sceneHasGoodEnoughDifference:
                            return (sceneGroup, minSceneNumber)
                        if currSceneIsMin:
                            currSceneIsMin = False
                            minSceneGroup = (
                                copy.copy(sceneGroup),
                                minSceneNumber,
                            )
                        sceneGroup = []
                    if "timestamp" in scene:
                        if (
                            scene["timestamp"][0] - latestTimestamp[0]
                            <= GOOD_ENOUGH_DIFFERENCE
                            or content["scene_number"] == 0
                        ):
                            sceneHasGoodEnoughDifference = True
                        elif minTime is None or scene["timestamp"][0] < minTime[0]:
                            minTime = scene["timestamp"]
                            minSceneNumber = content["scene_number"]
                            currSceneIsMin = True
                    currSceneNumber = content["scene_number"]
                    sceneGroup.append(scene)
    return minSceneGroup


def generateFill(line, lastScene, positions):
    transitionsInBetween = len(list(filter(lambda x: x[1] == "transition", positions)))
    fill = round(line["timestamp"][0] - lastScene["timestamp"][1], 2)
    if fill < 0 and not (
        line["timestamp"][0] == lastScene["timestamp"][0]
        or line["timestamp"][1] == lastScene["timestamp"][1]
    ):
        del line["timestamp"]
    elif fill - transitionsInBetween > 0:
        fill = round(
            (fill - (transitionsInBetween * 0.5)) / len(positions)
            if len(positions)
            else 0,
            2,
        )
    return fill


def fillInBetweenSceneLines(currScene, lastScene, positions):
    sceneIndex = 0
    TRANSITION = "transition"
    OTHER = "other"
    lastScene = copy.copy(lastScene)

    while sceneIndex < len(currScene[0]):
        line = currScene[0][sceneIndex]

        # defining fill timespan spread
        fill = generateFill(line, lastScene, positions) if "timestamp" in line else None
        if fill != None and fill > 0:
            # at last, fill in timestamps
            timestampRef = lastScene["timestamp"][1]
            for position in positions:
                if position[1] == TRANSITION:
                    position[0]["timestamp"] = [
                        timestampRef,
                        timestampRef + 0.5,
                    ]
                    timestampRef += 0.5
                elif position[1] == OTHER:
                    frodo = position[0]
                    position[0]["timestamp"] = [
                        timestampRef,
                        round(timestampRef + fill, 2),
                    ]
                    timestampRef = round(timestampRef + fill, 2)

            positions = []
            lastScene = {
                "scene_number": currScene[1],
                "timestamp": line["timestamp"],
                "scene": currScene[0],
            }
        elif isTransition(line):
            positions.append((line, TRANSITION))
        elif isCountCondition(line):
            if line["type"] == "ACTION" and "Nervous" in line["content"][0]["text"]:
                dfdf = 3
            positions.append((line, OTHER))
        sceneIndex += 1

    return (lastScene, positions)


def fillTimestamps(scriptWithTimestamp):
    positions = []
    currTagScenes = getScenesToBeTagged(scriptWithTimestamp)
    currentScene = None

    currentScene = getNextScene(scriptWithTimestamp, currTagScenes, [0, 0])
    lastScene = {"scene_number": 0, "timestamp": [0, 0]}

    # should increment initial scene right from the start
    currTagScenes[currentScene[1]] = False

    while currentScene:
        # fill timestamps between previous lines till there is a line with timestamps.
        # otherwise keep adding the list of lines to fill later
        (lastScene, positions) = fillInBetweenSceneLines(
            currentScene, lastScene, positions
        )
        # if all scenes have been covered, then quit
        done = True
        for key, val in currTagScenes.items():
            if val == True:
                done = False
                break
        if done:
            break

        # grab next scene
        currentScene = getNextScene(
            scriptWithTimestamp,
            currTagScenes,
            currentScene["timestamp"] if "timestamp" in currentScene else [0, 0],
        )

        if currentScene is None:
            break

        # increment scene's curr property in currTagScenes
        currTagScenes[currentScene[1]] = False
    return scriptWithTimestamp
