from flask import Flask, request, jsonify
import os
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import data_processor
import fetch_test_data

# Initialize Flask app
app = Flask(__name__)

# Initialize spaCy model
# nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("trainedModel")

# Function to generate embeddings
def generate_embeddings(data_directory):
    embeddings = []
    filenames = []

    # Iterate over resumes in the input directory
    for filename in os.listdir(data_directory):
        input_file_path = os.path.join(data_directory, filename)
        data_processor.preprocess_file(input_file_path)
        preprocessed_text = data_processor.preprocess_file(input_file_path)
        doc = nlp(preprocessed_text)
        embeddings.append(doc.vector)
        filenames.append(filename)
    
    return np.array(embeddings), filenames

# Function to generate embeddings for context
def generate_context_embeddings(context):
    preprocessed_text = data_processor.preprocess_text(context)
    job_doc = nlp(preprocessed_text)
    return job_doc.vector

# Function to fetch data from Cloud storage
def fetch_data_from_cloud(bucket_name, source_blob_prefix, destination_directory):
    fetch_test_data.download_files(bucket_name, source_blob_prefix, destination_directory)
    return destination_directory

# Function to calculate cosine similarity between jobs and resumes
def calculate_similarity(job_embeddings, resume_embeddings):
    return cosine_similarity(job_embeddings.reshape(1, -1), resume_embeddings)[0]

# Function to match embeddings
def match_job(context, input_embeddings, filenames, threshold, top_n):
    # Generate job embedding
    context_embedding = generate_context_embeddings(context)

    # Calculate cosine similarity
    similarity_scores = calculate_similarity(context_embedding, input_embeddings)

    # Convert similarity scores to a serializable format (Python list)
    similarity_scores_list = similarity_scores.tolist()

    # Rank based on similarity scores
    ranked_data = sorted(zip(filenames, similarity_scores_list), key=lambda x: x[1], reverse=True)

    # Filter matches based on threshold
    filtered_data = [(filename, score) for filename, score in ranked_data if score >= threshold]

    # Limit the number of matched data based on top_n
    matched_data = filtered_data[:top_n]

    return matched_data

@app.route('/')
def hello():
    return "Welcome to Recruitwise-AI"

@app.route('/search', methods=["GET"])
def searchGet():
    """Renders the search page."""
    output_string = "Get search invoked"
    return output_string

@app.route('/ping', methods=["GET"])
def ping():
    return "200"

# API endpoint to match resumes or jobs based on context
@app.route('/search', methods=['POST'])
def match():
    # Parse request parameters
    if not request.json or 'context' not in request.json or 'category' not in request.json or 'threshold' not in request.json or 'noOfMatches' not in request.json or 'inputPath' not in request.json:
        return jsonify({'error': 'Missing required parameters'}), 400

    context = request.json['context']
    category = request.json['category']
    threshold = float(request.json['threshold'])
    no_of_matches = int(request.json['noOfMatches'])
    input_path = request.json['inputPath']

    try:
        if category == 'resume':
            # Process resume recommendation
            # fetching data from input path and place in destination directory
            if input_path == 'https://console.cloud.google.com/storage/browser/hackathon1415':
                data = fetch_data_from_cloud(input_path, 'RESUME/data/', 'resumetrainingdata')
            else:
                data = fetch_data_from_cloud(input_path, '', 'resumes')
            
            resumes_directory = data  # resumes directory
            resumes_embeddings, filenames = generate_embeddings(resumes_directory)
            matched_resumes = match_job(context, resumes_embeddings, filenames, threshold, no_of_matches)
            response_data = [{'path': filename, 'score': score} for filename, score in matched_resumes]
            all_score = [job['score'] for job in response_data]
            conf_score = np.mean(all_score)
            if np.isnan(conf_score):
                conf_score = 0
        elif category == 'job':
            # Process job recommendation
            # fetching job data
            if input_path == 'https://console.cloud.google.com/storage/browser/hackathon1415':
                data = fetch_data_from_cloud(input_path, 'JD/', 'jobstrainingdata')
            else:
                data = fetch_data_from_cloud(input_path, '', 'jobs')
            
            job_description_directory = data  # job description directory
            # Placeholder for processing job data
            job_embeddings, filenames = generate_embeddings(job_description_directory)
            matched_jobs = match_job(context, job_embeddings, filenames, threshold, no_of_matches)
            response_data = [{'id': job_id, 'score': score} for job_id, score in matched_jobs]
            all_score = [job['score'] for job in response_data]
            conf_score = np.mean(all_score)
            if np.isnan(conf_score):
                conf_score = 0
        else:
            return jsonify({'error': 'Invalid category'}), 400

        return jsonify({
            'status': 'success',
            'count': len(response_data),
            'metadata': {'confidenceScore': conf_score},
            'results': response_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Main function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
