import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('ALL_VACANCY.xlsx')
# Extract the 'description' column for analysis to identify technical skills
job_descriptions = df['description'].dropna()

# Common technical skills to search for in descriptions
linkedin_skills = [
    # Programming Languages
    "Python", "JavaScript", "Java", " C++ ", "C#", "Ruby", "PHP", "Swift",
    "TypeScript", " Go ", " R ", "Kotlin", "SQL", "Rust", "MATLAB",

    # Web Development
    "HTML", "CSS", "JavaScript", "React.js", "Angular", "Vue.js", "SASS/SCSS",
    "Bootstrap", "Tailwind CSS", "Node.js", "Django", "Flask", "ASP.NET",
    "Ruby on Rails", "Next.js", "WebSockets",

    # Mobile Development
    "React Native", "Flutter", "Swift (iOS)", "Kotlin (Android)",
    "Java (Android)", "Xamarin", "Ionic",

    # Database Management
    "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Microsoft SQL Server",
    "Redis", "Cassandra", "Firebase Realtime Database", "DynamoDB",

    # Cloud and DevOps
    "AWS (Amazon Web Services)", "Microsoft Azure", "Google Cloud Platform (GCP)",
    "Docker", "Kubernetes", "Jenkins", "Terraform", "Ansible", "GitHub Actions",
    "CircleCI", "CloudFormation",

    # Data Analysis & Machine Learning
    "Pandas", "NumPy", "Matplotlib", "Scikit-learn", "TensorFlow", "PyTorch",
    "Keras", "Apache Spark", "Hadoop", "Tableau", "Power BI",

    # Version Control
    "Git", "GitHub", "GitLab", "Bitbucket",

    # Testing and Debugging
    "Selenium", "Cypress", "Jest", "Mocha", "JUnit", "Pytest",
    "Postman", "SoapUI", "Debugging Tools (Chrome DevTools, Xcode Debugger, etc.)",

    # Game Development
    "Unity", "Unreal Engine", "Godot", "CryEngine", "Cocos2d",

    # System Programming
    "Assembly", "Rust", " C ", "Kernel Development", "Embedded Systems",

    # Networking and Security
    "Linux Networking", "Wireshark", "OpenSSL", "Network Protocols (TCP/IP, HTTP/HTTPS)",
    "Penetration Testing Tools (Metasploit, Burp Suite)",
    "Firewalls and IDS/IPS", "Cryptography Libraries (PyCrypto, Bouncy Castle)",

    # Scripting
    "Shell Scripting (Bash, Zsh)", "PowerShell", "Perl", "TCL",

    # Artificial Intelligence and Data Science
    "Natural Language Processing (NLP)", "OpenCV (Computer Vision)",
    "Reinforcement Learning", "Time Series Analysis", "Deep Learning Frameworks",
    "AI Model Deployment (ONNX, TensorRT)",

    # Project Management Tools
    "JIRA", "Trello", "Asana", "Notion", "Monday.com",

    # API Development and Integration
    "RESTful APIs", "GraphQL", "gRPC", "Webhooks", "OAuth",

    # Others
    "WebAssembly", "Blockchain Development (Solidity, Ethereum, Hyperledger)",
    "IoT Development (Arduino, Raspberry Pi)",
    "ERP/CRM Systems (SAP, Salesforce)",

    # Technical Skills
    "Artificial Intelligence (AI) and Machine Learning",
    "Data Analysis and Interpretation",
    "Digital Literacy and Tech Proficiency",
    "Cybersecurity",
    "Cloud Computing",
    "Software Development",
    "Blockchain Technology",
    "Internet of Things (IoT)",
    "UX/UI Design",
    "Mobile Application Development",

    # Soft Skills
    "Critical Thinking and Problem-Solving",
    "Adaptability and Flexibility",
    "Emotional Intelligence",
    "Creativity and Innovation",
    "Communication and Collaboration",
    "Leadership and People Management",
    "Time Management",
    "Negotiation",
    "Decision-Making",
    "Stress Management",

    # Hybrid Skills
    "Digital Marketing",
    "Project Management",
    "Financial Management",
    "Sales and Business Development",
    "Strategic Planning",
    "Customer Service",
    "Content Creation",
    "Data Visualization",
    "SEO/SEM",
    "Supply Chain Management"
]

# Count the occurrence of each skill in the job descriptions
skill_counts = {skill: sum(job_descriptions.str.contains(skill, case=False)) for skill in linkedin_skills}

# Convert to a DataFrame for better readability and sort by frequency
skills_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Count']).sort_values(by='Count', ascending=False)
skills_df = skills_df[skills_df['Count'] > 0]
skills_df.to_excel('summary_skills.xlsx')
plt.bar(skills_df["Skill"], skills_df["Count"], color='violet')
plt.show()

#tools.display_dataframe_to_user(name="Technical Skills Frequency", dataframe=skills_df)


