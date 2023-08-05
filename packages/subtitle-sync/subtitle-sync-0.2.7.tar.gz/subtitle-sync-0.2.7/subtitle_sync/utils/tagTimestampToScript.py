def tagTimestampToScript(pureScript, scriptWithTimestamp):
    for line in scriptWithTimestamp:
        if "timestamp" in line:
            pureScript[line["pageIndex"]]["content"][line["sceneIndex"]]["scene"][
                line["sectionIndex"]
            ]["timestamp"] = [line["timestamp"][0], line["timestamp"][1]]

            pureScript[line["pageIndex"]]["content"][line["sceneIndex"]]["scene"][
                line["sectionIndex"]
            ]["sceneOrder"] = line["sceneOrder"]

            """
            remaining words in the left bumps the start timestamp
            remaining words in the right bumps the end timestamp
            """
    return pureScript
