import pdfplumber
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EnhancedResumeScanner:
    def _init_(self, keywords):
        self.keywords = keywords

    def extract_text_from_pdf(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + ' '
        return text.strip()

    def extract_information(self, resume_text):
        # Regular expressions for extracting user details
        name_regex = r'^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+'
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_regex = r'(?<!\d)(\d{10})(?!\d)'

        name_match = re.search(name_regex, resume_text, re.MULTILINE)
        email_match = re.search(email_regex, resume_text)
        phone_match = re.search(phone_regex, resume_text)

        name = name_match.group(0) if name_match else 'Not found'
        email = email_match.group(0) if email_match else 'Not found'
        phone = phone_match.group(0) if phone_match else 'Not found'

        # Extract skills (case insensitive)
        skills_found = [skill for skill in self.keywords if skill.lower() in resume_text.lower()]
        
        return {
            'Name': name,
            'Email': email,
            'Phone': phone,
            'Skills': skills_found
        }

    def calculate_similarity(self, resume_text):
        # Prepare documents for vectorization
        documents = [' '.join(self.keywords), resume_text]
        
        # Vectorization
        vectorizer = CountVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()

        # Calculate cosine similarity
        cosine_sim = cosine_similarity(vectors)
        return cosine_sim[0][1]  # similarity between keywords and resume

    def scan_resume(self, pdf_path):
        resume_text = self.extract_text_from_pdf(pdf_path)
        info = self.extract_information(resume_text)
        similarity_score = self.calculate_similarity(resume_text)

        return {
            'Info': info,
            'Similarity Score': similarity_score
        }

# Example usage
if _name_ == "_main_":
    # Define a list of general keywords/skills
    general_keywords = [
        'Python', 'Machine Learning', 'Data Analysis',
        'Project Management', 'Teamwork', 'Communication', 'Cloud Computing',
        'Problem Solving', 'Algorithms', 'Data Structures', 'Statistics' ,'C#','Python', 'Java', 'C++', 'JavaScript', 'Ruby', 'R', 'Go', 'Swift', 'Kotlin',
        'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'Django', 'Flask',
        'Machine Learning', 'Data Analysis', 'Data Visualization', 'SQL', 
        'Pandas', 'NumPy', 'TensorFlow', 'PyTorch', 'Statistics',
        'AWS', 'Azure', 'Google Cloud Platform', 'Docker', 'Kubernetes',
        'Git', 'Jenkins', 'Terraform', 'Ansible',
        'Project Management', 'Agile Methodologies', 'Scrum', 'Teamwork', 
        'Communication', 'Problem Solving', 'Time Management', 'Leadership',
        'Network Security', 'Penetration Testing', 'Ethical Hacking', 'Risk Assessment',
        'Algorithms', 'Data Structures', 'Blockchain', 'Internet of Things (IoT)', 
        'UX/UI Design'

    ]

    scanner = EnhancedResumeScanner(keywords=general_keywords)
    
    # Replace 'resume.pdf' with the path to your resume PDF
    result = scanner.scan_resume('C:/Users/Rohan/OneDrive/Desktop/mini/resume/resume.pdf')
    
    print("Extracted Information:")
    print(f"Name: {result['Info']['Name']}")
    print(f"Email: {result['Info']['Email']}")
    print(f"Phone: {result['Info']['Phone']}")
    print(f"Skills: {', '.join(result['Info']['Skills'])}")
    print(f"Similarity Score: {result['Similarity Score']:.2f}")