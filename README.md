# **WebWeave: Instagram Social Connection Analyzer**

## **Overview**

WebWeave is a powerful tool designed to map and analyze social connections on Instagram. By scraping follower and following data, WebWeave allows users to visualize relationships in a graph format, making it ideal for personal networking, social analysis, and even influencer research.

## **Use Cases**

### **1. Personal Social Analysis**

Ever wondered how you are connected to different people on Instagram? WebWeave helps you see your direct and indirect connections, giving you insights into mutual relationships and how different social circles intersect.

### **2. Influencer Research**

Brands and marketers can use WebWeave to analyze an influencer’s network, identifying key mutual connections, potential collaborations, and assessing their engagement reach.

### **3. Competitive Analysis**

Businesses can scrape competitor social graphs to understand their audience overlap and find potential customers who follow multiple competitors.

### **4. Network Growth Strategy**

Want to grow your social presence? WebWeave can help you identify key people to connect with by analyzing the common followers of influential users in your niche.

---

## **Installation & Setup**

### **1. Install Dependencies**

Ensure you have Python installed, then install the required dependencies using:

```bash
pip install -r requirements.txt
```

### **2. Logging in to Instagram**

- If a login session exists (stored via cookies), WebWeave will automatically authenticate.
- If no session is found, you will be prompted to enter your **username and password**.
- Once logged in, WebWeave saves the session, so you won’t need to log in again unless the session expires.

### **3. Scraping a Target’s Network**

To analyze a user's network:

1. Enter the **Instagram username** (must be accurate).
2. Provide the **person’s actual name** (for reference purposes).
3. WebWeave will scrape the user's **followers and followings**, storing them in a PostgreSQL database.

You can scrape as many users as needed to expand your network visualization.

### **4. Visualizing the Network**

Once data is collected, generate the social graph with:

```bash
python visualize.py
```

This will open an interactive visualization of the network, showing connections between users.

---

## **Key Features**

✅ **Automated Instagram Login** – Saves session cookies for seamless future logins.\
✅ **Scrapes Followers & Followings** – Extracts and stores user data for analysis.\
✅ **PostgreSQL Integration** – Efficiently handles large-scale social graphs.\
✅ **Graph Visualization** – Easily interpret relationships with a dynamic network view.\
✅ **Scalable & Reusable** – Continuously expand and update the dataset with new users.

---

## **Future Enhancements**

🚀 **Mutual Connection Filtering** – Highlight only bidirectional relationships.\
🚀 **Edge Weighting** – Prioritize connections based on interaction frequency.\
🚀 **Advanced Search & Filtering** – Find users based on shared connections or influence levels.

---

## **Contributing**

Want to improve WebWeave? Feel free to fork the repo, submit pull requests, or suggest features.

**Happy networking!** 🚀

