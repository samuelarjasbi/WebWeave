from auth import SeleniumSession
from scraper import JSInjector
from user_data_handler import UserDataHandler

# Initialize session manager for a website
session = SeleniumSession(url="https://instagram.com", cookies_file="cookies1.pkl", username="saraakhavan_official", password="Mm@@82651")

# Start session (loads cookies if available, otherwise prompts login)
session.start_session()

js_injector = JSInjector(session)

username = str(input("Enter the handle to scrape: "))
full_name = str(input("Enter user name: "))
scrape_option = input("Choose what to scrape (followers / followings / both): ").strip().lower()

# JS script with conditional scraping logic
script = """
const username = "USER_NAME_HERE";
const scrapeType = "SCRAPE_TYPE_HERE";
const callback = arguments[arguments.length - 1];
(async () => {
  try {
    console.log(`Process started! Give it a couple of seconds`);
    let followers = [];
    let followings = [];
  
    // Fetch user data to get userId
    const userQueryRes = await fetch(
      `https://www.instagram.com/web/search/topsearch/?query=${username}`
    );
    const userQueryJson = await userQueryRes.json();
    const userId = userQueryJson.users.map(u => u.user)
                                        .filter(u => u.username === username)[0].pk;
  
    if (scrapeType === "both" || scrapeType === "followers") {
      // Fetch followers
      let after = null;
      let has_next = true;
      while (has_next) {
        const res = await fetch(
          `https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=` +
            encodeURIComponent(JSON.stringify({
              id: userId,
              include_reel: true,
              fetch_mutual: true,
              first: 50,
              after: after,
            }))
        );
        const json = await res.json();
        has_next = json.data.user.edge_followed_by.page_info.has_next_page;
        after = json.data.user.edge_followed_by.page_info.end_cursor;
        followers = followers.concat(
          json.data.user.edge_followed_by.edges.map(({ node }) => ({
            username: node.username,
            full_name: node.full_name,
          }))
        );
      }
      console.log({ followers });
    }
  
    if (scrapeType === "both" || scrapeType === "followings") {
      // Fetch followings
      let after = null;
      let has_next = true;
      while (has_next) {
        const res = await fetch(
          `https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=` +
            encodeURIComponent(JSON.stringify({
              id: userId,
              include_reel: true,
              fetch_mutual: true,
              first: 50,
              after: after,
            }))
        );
        const json = await res.json();
        has_next = json.data.user.edge_follow.page_info.has_next_page;
        after = json.data.user.edge_follow.page_info.end_cursor;
        followings = followings.concat(
          json.data.user.edge_follow.edges.map(({ node }) => ({
            username: node.username,
            full_name: node.full_name,
          }))
        );
      }
      console.log({ followings });
    }
  
    // Process comparisons only if both lists are scraped
    let dontFollowMeBack = [];
    let iDontFollowBack = [];
    if (scrapeType === "both") {
      dontFollowMeBack = followings.filter(following =>
        !followers.find(follower => follower.username === following.username)
      );
      console.log({ dontFollowMeBack });
  
      iDontFollowBack = followers.filter(follower =>
        !followings.find(following => following.username === follower.username)
      );
      console.log({ iDontFollowBack });
    }
  
    // Final callback with the results
    callback({
      followers: followers,
      followings: followings,
      dontFollowMeBack: dontFollowMeBack,
      iDontFollowBack: iDontFollowBack
    });
  } catch (err) {
    callback({ error: err.toString() });
  }
})();
"""

# Replace placeholders with actual values
script = script.replace('USER_NAME_HERE', username)
script = script.replace('SCRAPE_TYPE_HERE', scrape_option)

input("Enter when Instagram is fully loaded")
result = js_injector.execute_async_script(script)
print(result)

user_handler = UserDataHandler()
# Retrieve data; note that one of these may be empty if not scraped
followers = result.get('followers', [])
followings = result.get('followings', [])

user_handler.enter_user_info(username, full_name, followings, followers)

# Close the database session
user_handler.close()

print(f"Total followers: {len(followers)}")
print(f"Total followings: {len(followings)}")

# If both lists exist, do comparisons
if scrape_option == "both":
    followers_usernames = {f['username'] for f in followers}
    followings_usernames = {f['username'] for f in followings}

    common_usernames = followers_usernames & followings_usernames

    followers_filtered = [f for f in followers if f['username'] not in common_usernames]
    followings_filtered = [f for f in followings if f['username'] not in common_usernames]

    total_unique = len(followers_filtered) + len(followings_filtered)
    print(f"Total unique elements: {total_unique}")

# Close the session when done
session.close()
