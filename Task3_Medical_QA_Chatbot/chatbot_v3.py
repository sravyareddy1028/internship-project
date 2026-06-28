import os
import xml.etree.ElementTree as ET

questions = []
answers = []

folder_path = r"C:\Users\Sravya Reddy\Downloads\MedQuAD-master.zip\MedQuAD-master\1_CancerGov_QAs\CancerGov_QAs"

print("Reading dataset...")

for root_dir, dirs, files in os.walk(folder_path):

    for filename in files:

        if filename.endswith(".xml"):

            file_path = os.path.join(root_dir, filename)

            print("Reading:", file_path)

            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Find all Question and Answer pairs
                for qa in root.iter():

                    if qa.tag.lower() == "qapair":

                        question = qa.find("Question")
                        answer = qa.find("Answer")

                        if question is not None and answer is not None:

                            if question.text and answer.text:

                                questions.append(question.text.strip())
                                answers.append(answer.text.strip())

            except Exception as e:
                print(f"Error in {filename}: {e}")

print(f"\nTotal Questions Loaded: {len(questions)}")
print(f"Total Answers Loaded: {len(answers)}")

if len(questions) == 0:
    raise Exception("No questions were loaded. Check the dataset path or XML structure.")