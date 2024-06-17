import streamlit as st

def main():
    st.title("About Me: Darshan Chinvar Prakash")

    st.header("Contact Information")
    st.write("**Location:** Irvine, CA")
    st.write("**Email:** [chinvarpd@gmail.com](mailto:chinvarpd@gmail.com)")
    st.write("**LinkedIn:** [linkedin.com/in/chinvar](https://linkedin.com/in/chinvar)")

    st.header("Summary")
    st.write("""
    With vast experience in Software Engineering, AI/ML, Generative AI, Enterprise Cloud Solutions and Architecture, I am an accomplished professional aspiring to expand my vocational sphere to achieve higher goals.
    - Directing the integration of Generative AI across various business sectors, including Investment Group, Fixed Income, Enterprise Data Office, Legal, and HR at Capital Group.
    - Spearheading GenAI developer platform for data scientists and engineers, evaluating models from Azure AI Services (OpenAI, GPT models), Databricks, Azure ML Studio, and AWS SageMaker plus Bedrock.
    - Pioneering LLMOps and MLOps architecture with comprehensive governance, encompassing machine learning pipelines, feature engineering, model deployment and monitoring, as well as batch and real-time inferencing.
    - Influencing company’s strategic direction and business technology roadmap through analysis and research on emerging trends for potential impact on product lifecycle management in a multi-cloud platform.
    - Facilitating cloud governance in a financial services company, exceeding security and compliance standards expectations, and conducting security reviews to identify and address any gaps in security posture.
    - Expert in OOP, algorithms, and data structures, with experience in designing scalable microservices and serverless applications using .Net Core and Python, following SAFE agile and scrum methodologies.
    - Championing container initiatives (ECS, EKS in AWS; ACI, AKS in Azure) and creating a reusable automation framework (Terraform, Ansible, Puppet, Helm, CloudFormation, ARM template, CDK) for product domains.
    - Developed observability solutions for GenAI and microservices apps to monitor performance and cost chargeback.
    - Championing diversity, inclusivity, and equitable opportunities within the workplace, I fervently advocate for a culture that encourages continuous feedback and upholds engineering excellence.
    """)

    st.header("Work Experience")

    st.subheader("Capital Group | Lead Cloud Software Engineer | Irvine, CA | Oct 2019 – Present")
    st.write("""
    - Leading a team of AI researchers and developers focused on Gen AI monetization, I excel in driving cross-functional initiatives and integrating generative AI into products to drive revenue. Key achievements include creating a strategic roadmap, demoing solutions to senior leadership, raising multi-million dollar funding, and building a high-performing team by hiring the right talent.
    - Spearheaded development of AI-driven Copilot, Virtual Assistants and Chatbots using Python, Streamlit, Lang Chain, LlamaIndex, RAG, agentic LLM apps, vector databases, prompt engineering to cater to a diverse range of stakeholders, including developer productivity tools.
    - Collaborated with Microsoft and AWS to understand data processing and storage; worked with InfoSec to establish abuse monitoring and content filtering, ensuring the integrity and security of our Gen AI solutions.
    - Managed model endpoints for live and batch inferencing, implementing robust security with private endpoints, virtual networks, and prompt logging for audit, ensuring information security and operational efficiency.
    - Designed and developed comprehensive monitoring dashboards, focusing on key metrics such as latency, performance, and availability, to ensure optimal functioning and continuous improvement of LLM applications.
    - Engineered an enterprise-ready Azure Landing Zone solution incorporating scale, security, governance, networking, and identity, facilitating IT portfolio support including hybrid connectivity, and expedited account creation; also implemented Azure policies and blueprints ensuring business continuity, disaster recovery requirements, and auto-remediation of non-compliant services with log forwarding to Splunk.
    - Spearheaded the development of an enterprise CI/CD platform for AWS and Azure, enabling hundreds of developers to manage thousands of pipelines and implemented Infrastructure as Code using Terraform.
    - Created reference architecture and Service Catalog for various cloud solutions with enterprise-level security, including SageMaker, ECS, ACI, AKS clusters, and node pools, while also supporting a hybrid Kubernetes platform in OpenShift Container Platform.
    """)

    st.subheader("Western Digital | Principal Software DevOps Engineer | Irvine, CA | Oct 2018 – Oct 2019")
    st.write("""
    - Led software architecture design and project implementation across teams, streamlining the software development lifecycle with CI/CD processes using Git, Jenkins, and Docker.
    - Developed applications and frameworks for efficient code development, validation, and adherence to coding standards, boosting developer productivity and code quality.
    - Maintained stability and reliability of build and continuous integration environments, supporting over 5000 daily build jobs, and automated metrics and dashboards for real-time insights, implementing alerting mechanisms and incident response procedures.
    """)

    st.subheader("Experian | Software Development Specialist II | Costa Mesa, CA | Jan 2012 – Sep 2018")
    st.write("""
    - Created orchestrated tools using serverless apps to scale over 500 microservices handling live traffic in AWS.
    - Designed and implemented highly scalable RESTful APIs using .NET Core and Python for microservices and serverless applications, contributing to the deployment of reliable cloud-based distributed systems.
    - Led the transition from a monolithic application to a .NET Core microservices architecture on AWS.
    - Played a key role in a $20 million, 2-year cloud migration project, transitioning from on-premises to AWS.
    - Engineered a Python application (Infrastructure as a Service) using Boto3 API and CloudFormation, supporting the deployment of microservices across various programming languages in AWS.
    - Developed a robust CI/CD pipeline using GitHub, Jenkins, and Travis CI, automating the integration and deployment of .NET/Java microservices and Python container applications on AWS.
    - Provided mentorship and training in Docker, Nginx, service discovery, service versioning, and scaling.
    - Demonstrated a strong customer focus by collaborating with application teams to assist with architecture and design patterns, and by facilitating the onboarding of internal customers to AWS and Azure cloud platforms.
    """)

    st.subheader("Network Enhanced Technologies | Software Developer Intern | Los Angeles, CA | June 2010 – Dec 2011")
    st.write("""
    - Developed "Auto Invoice" using .NET and SQL2008 to automate invoice generation and delivery, integrating with Intuit QuickBooks SDK, resulting in thousands of invoices being automatically created and emailed.
    """)

    st.header("Educational Qualifications")
    st.write("""
    - **California State University - Long Beach, USA** | MS in Computer Science | Dec 2011
    - **Visweswaraya Technological University, India** | BE in Computer Science | Aug 2008
    """)

    st.header("Professional Skills")
    st.write("""
    - **Cloud Expertise and Certifications:**
        - AWS: Certified Machine Learning – Specialty, Certified Solutions Architect – Professional
        - Microsoft Azure: Solutions Architect – Expert
        - Google Cloud Platform (GCP): Associate Cloud Engineer
    - **AI/ML:** MLOps, LLMOps, Databricks, Azure ML, SageMaker, JumpStart, AWS Bedrock
    - **Gen AI:** Lang Chain, Lang Smith, Lang Flow, Prompt Flow, Llama Index
    - **Containerization:** Docker, AWS ECS/EKS, Microsoft ACI/AKS, Kubernetes
    - **Programming and Scripting:** Python, C#, Shell 
    - **Automation Frameworks:** Terraform, Puppet, Ansible, Control-M, CloudFormation, CDK, ARM
    - **CI/CD:** Git, Maven, Nuget, Jenkins, TravisCI, Atlassian suite, Code Pipeline, Code Build, Azure DevOps
    - **Observability:** TwistLock, DataDog, Splunk, Cloudability, Azure Monitor, CloudWatch
    - **Governance:** Azure Policies, Initiatives and Blueprints, AWS SCP/conformance packs
    - **AWS Expertise:** ECR, Lambda, Step Functions, API Gateway, CloudWatch, Config, Service Catalog, EC2, EBS, SQS, SNS, VPC, DynamoDB, Aurora, CloudFront, Route 53, WAF, KMS, S3, Backup Vault, Organizations
    - **Azure Expertise:** ACR, Functions, Logic Apps, API Management, Event Hubs, vNet, Data Lake, DNS, Firewall, Defender, Key Vault, Storage Accounts, Recovery Service Vaults, Management Groups
    """)

if __name__ == "__main__":
    main()
