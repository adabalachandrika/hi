from cgitb import reset
import os
import json


# assign directory
startpath = '.'
ouptutPath = os.path.join(os.getcwd(), 'output')


def create_output_dir(ouptutPath):
    if not os.path.exists(ouptutPath):
        os.makedirs(ouptutPath)


def main():
    for root, dirs, files in os.walk(startpath):
        for mainDir in dirs:
            print("Processing directory: " + mainDir)
            curOuptutPath = os.path.join(ouptutPath, mainDir)
            go_inside = os.path.join(startpath, mainDir)
            for root, dirs, files in os.walk(go_inside):
                result = {'total_results': 0, 'messages': []}
                messages = []
                for subDir in dirs:
                    print("\tProcessing sub-directory: " + subDir)
                    curOuptutPath = os.path.join(ouptutPath, mainDir, subDir)
                    create_output_dir(curOuptutPath)
                    count = 0
                    for file in os.listdir(os.path.join(startpath, mainDir, subDir)):
                        if(file.endswith('.json')):
                            count += 1
                            with open(os.path.join(startpath, mainDir, subDir, file), 'r') as infile:
                                data = json.load(infile)
                                result["total_results"] += data["total_results"]
                                for message in data["messages"]:
                                    message = message[0]
                                    del message["attachments"]
                                    del message["embeds"]
                                    del message["mentions"]
                                    del message["mention_roles"]
                                    del message["tts"]
                                    del message["pinned"]
                                    del message["edited_timestamp"]
                                    del message["mention_everyone"]
                                    del message["flags"]
                                    del message["components"]
                                    del message["hit"]
                                    # add message object to result
                                    result["messages"].append(message)
                                    # add message content to list
                                    messages.append(message["content"])

                    print("\t\tProcessed " + str(count) + " files")
                    print("\t\tSub Dir Final results: " +
                          str(result["total_results"]))

                    if(result["total_results"] > 0):
                        with open(os.path.join(curOuptutPath, 'merged.json'), 'w') as outfile:
                            print("\t\tRoot Dir Final results: " +
                                  str(result["total_results"]))
                            json.dump(result, outfile)
                        print("\t\tSaved merged.json")
                        outfile.close()
                        with open(os.path.join(curOuptutPath, 'merged.txt'), 'w') as outfile:
                            for line in messages:
                                outfile.write(line)
                                outfile.write('\n')
                        print("\t\tSaved merged.txt")
                        outfile.close()


if __name__ == '__main__':
    main()
