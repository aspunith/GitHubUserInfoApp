import streamlit as st
import requests

def fetch_github_user_data(username, token):
    base_url = "https://api.github.com/users/"
    headers = {"Authorization": f"token {token}"} if token else {}

    # Fetch user details
    user_response = requests.get(f"{base_url}{username}", headers=headers)
    if user_response.status_code != 200:
        return {"error": f"Error: {user_response.status_code} - {user_response.json().get('message', 'Unknown error')}"}

    user_data = user_response.json()

    # Fetch repositories
    repos_response = requests.get(f"{base_url}{username}/repos", headers=headers)
    if repos_response.status_code != 200:
        return {"error": f"Error: {repos_response.status_code} - {repos_response.json().get('message', 'Unknown error')}"}

    repos_data = repos_response.json()

    # Extract languages used in each repo
    languages = {}
    for repo in repos_data:
        lang_url = repo["languages_url"]
        lang_response = requests.get(lang_url, headers=headers)
        if lang_response.status_code == 200:
            languages[repo["name"]] = list(lang_response.json().keys())

    return {
        "name": user_data.get("name"),
        "public_repos": user_data.get("public_repos"),
        "followers": user_data.get("followers"),
        "languages": languages,
        "contributions_calendar": f"https://github.com/{username}"  # Link to contributions calendar
    }

def main():
    st.title("GitHub User Info Fetcher")

    # Input fields
    username = st.text_input("Enter GitHub Username:")
    token = st.text_input("Enter GitHub Personal Access Token (optional):", type="password")

    if st.button("Fetch Data"):
        if not username:
            st.error("Please enter a GitHub username.")
        else:
            with st.spinner("Fetching data..."):
                data = fetch_github_user_data(username, token)

            if "error" in data:
                st.error(data["error"])
            else:
                st.subheader("User Details")
                st.write(f"**Name:** {data['name']}")
                st.write(f"**Public Repositories:** {data['public_repos']}")
                st.write(f"**Followers:** {data['followers']}")

                st.subheader("Languages Used in Repositories")
                for repo, langs in data["languages"].items():
                    st.write(f"**{repo}:** {', '.join(langs) if langs else 'No languages detected'}")

                st.subheader("Contributions Calendar")
                st.markdown(f"[View Contributions Calendar]({data['contributions_calendar']})")

if __name__ == "__main__":
    main()
