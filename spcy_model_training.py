import os
import spacy
from spacy.training import Example
import data_processor
import re

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a file
def extract_text_from_file(file_path):
    preporcessed_text = data_processor.preprocess_file(file_path)
    return preporcessed_text

# Function to annotate text with named entities
def annotate_text_frm_file(text):
    annotations = []

    # Define keywords and their corresponding entity labels
    keyword_labels = {
        "experience": "EXPERIENCE",
        "work history": "EXPERIENCE",
        "employment": "EXPERIENCE",
        "skills": "SKILL",
        "competencies": "SKILL",
        "education": "EDUCATION",
        "qualification": "EDUCATION",
        "degree": "EDUCATION",
        "certification": "EDUCATION"
    }

    # Search for entities in the entire text
    for keyword, label in keyword_labels.items():
        matches = re.finditer(rf"\b{re.escape(keyword)}\b", text, flags=re.IGNORECASE)
        for match in matches:
            start_index = match.start()
            end_index = match.end()
            annotations.append((start_index, end_index, label))

    return annotations

# Function to prepare training examples from resumes and job descriptions
def prepare_training_data(directory):
    train_data = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        text = extract_text_from_file(file_path)
        annotations = annotate_text_frm_file(text)
        train_data.append((text, {"entities": annotations}))
    return train_data

def train_ner_model(train_data):
    for text, annotations in train_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example])
    return nlp

def save_model(nlp, output_dir):
    nlp.to_disk(output_dir)
    print(f"Trained NER model saved to {output_dir}")

def main():
    # Paths to directories containing resumes and job descriptions
    resumes_directory = "resumetrainingdata"
    jobs_directory = "jobstrainingdata"

    # Prepare training data
    resumes_train_data = prepare_training_data(resumes_directory)
    jobs_train_data = prepare_training_data(jobs_directory)
    combined_train_data = resumes_train_data + jobs_train_data

    # Train NER model
    nlp = train_ner_model(combined_train_data)

    # Save trained model
    output_dir = "trainedModel"
    save_model(nlp, output_dir)

if __name__ == "__main__":
    main()