from academics_agent.database import save_snippet, init_db

def seed():
    init_db()
    
    print("Saturating the Librarian with fictional academic data...")
    
    save_snippet("Project Aether", "Aether is a decentralized satellite-to-ground mesh network protocol using LoRa technology for disaster zones.")
    save_snippet("Project Titan-V", "Titan-V is an autonomous rover navigation system using LIDAR and SLAM algorithms for subterranean mapping.")
    
    save_snippet("Advanced Algorithms", "The Final Exam on May 15th covers NP-Hard problems, Bellman-Ford, and Red-Black Trees.")
    save_snippet("Cyber-Physical Systems", "Lab 4 requires a PID controller implementation for a self-balancing drone.")
    save_snippet("Distributed Systems", "The research paper on 'Byzantine Fault Tolerance' is due next Friday at midnight.")
    
    save_snippet("Quantum Cryptography", "Quantum Key Distribution (QKD) is the primary focus of the Phase 2 research grant.")
    save_snippet("Machine Learning", "The model for the Sign Language Translator needs to be retrained with a higher dropout rate to prevent overfitting.")
    save_snippet("Ethics in AI", "Review the 'Algorithmic Bias' chapter for the upcoming debate on Monday.")
    
    # 4. Schedule/Deadline Notes
    save_snippet("Internship Hunt", "Update the portfolio with the React-Native finance app before applying to the Google APAC program.")
    save_snippet("Thesis Progress", "Met with Dr. Sharma; need to refine the methodology section for the 'Neural-Link' simulation by tomorrow.")

    print("✅ Memory Overloaded! The Librarian is now an expert on fictional academics.")

if __name__ == "__main__":
    seed()