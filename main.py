from auth import SeleniumSession
from scraper import JSInjector
from user_data_handler import UserDataHandler
# Initialize session manager for a website
session = SeleniumSession(url="https://instagram.com", cookies_file="cookies1.pkl", username="saraakhavan_official", password="Mm@@82651")

# Start session (loads cookies if available, otherwise prompts login)
session.start_session()


js_injector = JSInjector(session)



username = str(input("enter the handle to scrape: "))
full_name = str(input("enter user name: "))

script = """
const username = "USER_NAME_HERE";
const callback = arguments[arguments.length - 1];
(async () => {
  try {
    console.log(`Process started! Give it a couple of seconds`);
    let followers = [];
    let followings = [];
    let dontFollowMeBack = [];
    let iDontFollowBack = [];
  
    // Fetch user data to get userId
    const userQueryRes = await fetch(
      `https://www.instagram.com/web/search/topsearch/?query=${username}`
    );
    const userQueryJson = await userQueryRes.json();
    const userId = userQueryJson.users.map(u => u.user)
                                        .filter(u => u.username === username)[0].pk;
  
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
  
    // Fetch followings
    after = null;
    has_next = true;
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
  
    // Process comparisons
    dontFollowMeBack = followings.filter(following =>
      !followers.find(follower => follower.username === following.username)
    );
    console.log({ dontFollowMeBack });
  
    iDontFollowBack = followers.filter(follower =>
      !followings.find(following => following.username === follower.username)
    );
    console.log({ iDontFollowBack });
  
    // Final callback with the results
    callback({
      followers: followers,
      followings: followings,
      dontFollowMeBack: dontFollowMeBack,
      iDontFollowBack: iDontFollowBack
    });
  } catch (err) {
    // In case of error, pass it via the callback
    callback({ error: err.toString() });
  }
})();
"""

script = script.replace('USER_NAME_HERE',username)

input("enter when instagram is fully loaded")
result = js_injector.execute_async_script(script)
print(result)



user_handler = UserDataHandler()
# Correct the assignments
followers = result['followers']  # Users following the target
followings = result['followings']  # Users the target follows



user_handler.enter_user_info(username, full_name, followings, followers)

# Close the database session
user_handler.close()
# Do your automated tasks here...


print(f"total followers {len(followers)}")
print(f"total followings {len(followings)}")

# Extracting the usernames from both lists
followers_usernames = {f['username'] for f in followers}
followings_usernames = {f['username'] for f in followings}

# Find common usernames
common_usernames = followers_usernames & followings_usernames

# Remove the common items from both lists
followers_filtered = [f for f in followers if f['username'] not in common_usernames]
followings_filtered = [f for f in followings if f['username'] not in common_usernames]

# Calculate the total number of unique elements
total_unique = len(followers_filtered) + len(followings_filtered)

print(f"Total unique elements: {total_unique}")


# Close the session when done
session.close()