import streamlit as st
import asyncio
import pandas as pd
from datetime import datetime
from ..client.base import HubClient

st.set_page_config(
    page_title="JupyterHub Manager", 
    layout="wide",
    page_icon="🚀"
)

st.title("🚀 JupyterHub Manager")
st.markdown("Professional admin interface for JupyterHub management")

# Initialize session state
if 'users' not in st.session_state:
    st.session_state.users = []
if 'groups' not in st.session_state:
    st.session_state.groups = []
if 'services' not in st.session_state:
    st.session_state.services = []

@st.cache_resource
def get_client():
    return HubClient()

client = get_client()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", [
    "Dashboard", "Users", "Groups", "Servers", "Services", "Tokens", "Admin"
])

# Helper functions
async def fetch_users():
    try:
        return await client.list_users()
    except Exception as e:
        st.error(f"Error fetching users: {e}")
        return []

async def fetch_groups():
    try:
        return await client.list_groups()
    except Exception as e:
        st.error(f"Error fetching groups: {e}")
        return []

async def fetch_services():
    try:
        return await client.list_services()
    except Exception as e:
        st.error(f"Error fetching services: {e}")
        return []

async def fetch_health():
    try:
        return await client.get_health()
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Dashboard page
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Health status
    with col1:
        health = asyncio.run(fetch_health())
        status = health.get("status", "unknown")
        if status == "ok":
            st.success("🟢 Hub Status: Healthy")
        else:
            st.error(f"🔴 Hub Status: {status}")
    
    # Quick stats
    with col2:
        users = asyncio.run(fetch_users())
        st.metric("Total Users", len(users))
    
    with col3:
        active_servers = sum(1 for u in users if u.get("servers"))
        st.metric("Active Servers", active_servers)
    
    with col4:
        admin_users = sum(1 for u in users if u.get("admin"))
        st.metric("Admin Users", admin_users)
    
    # Recent activity chart
    st.subheader("Recent Activity")
    if users:
        df = pd.DataFrame(users)
        if 'last_activity' in df.columns:
            df['last_activity'] = pd.to_datetime(df['last_activity'], errors='coerce')
            df = df.dropna(subset=['last_activity'])
            if not df.empty:
                st.line_chart(df.set_index('last_activity').resample('D').size())
            else:
                st.info("No recent activity data available")
        else:
            st.info("Activity data not available")

# Users page
elif page == "Users":
    st.header("👥 User Management")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Refresh Users"):
            st.session_state.users = asyncio.run(fetch_users())
            st.success("Users refreshed!")
    
    with col1:
        search_term = st.text_input("🔍 Search users", placeholder="Enter username...")
    
    # Create new user
    with st.expander("➕ Create New User"):
        with st.form("create_user_form"):
            new_username = st.text_input("Username")
            is_admin = st.checkbox("Admin privileges")
            
            if st.form_submit_button("Create User"):
                try:
                    result = asyncio.run(client.create_user(new_username, is_admin))
                    st.success(f"✅ Created user: {new_username}")
                    st.session_state.users = asyncio.run(fetch_users())
                except Exception as e:
                    st.error(f"❌ Error creating user: {e}")
    
    # Display users
    users = st.session_state.users or asyncio.run(fetch_users())
    
    if search_term:
        users = [u for u in users if search_term.lower() in u.get("name", "").lower()]
    
    if users:
        for user in users:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                
                with col1:
                    admin_badge = "👑" if user.get("admin") else "👤"
                    st.write(f"{admin_badge} **{user.get('name')}**")
                
                with col2:
                    server_status = "🟢 Running" if user.get("servers") else "⚪ Stopped"
                    st.write(server_status)
                
                with col3:
                    if st.button("▶️ Start", key=f"start_{user['name']}"):
                        try:
                            asyncio.run(client.start_server(user["name"]))
                            st.success("Server starting...")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col4:
                    if st.button("⏹️ Stop", key=f"stop_{user['name']}"):
                        try:
                            asyncio.run(client.stop_server(user["name"]))
                            st.success("Server stopping...")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col5:
                    if st.button("🗑️ Delete", key=f"delete_{user['name']}"):
                        try:
                            asyncio.run(client.delete_user(user["name"]))
                            st.success("User deleted!")
                            st.session_state.users = asyncio.run(fetch_users())
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                st.divider()
    else:
        st.info("No users found")

# Groups page
elif page == "Groups":
    st.header("👥 Group Management")
    
    if st.button("🔄 Refresh Groups"):
        st.session_state.groups = asyncio.run(fetch_groups())
        st.success("Groups refreshed!")
    
    # Create new group
    with st.expander("➕ Create New Group"):
        with st.form("create_group_form"):
            group_name = st.text_input("Group Name")
            initial_users = st.text_area("Initial Users (one per line)")
            
            if st.form_submit_button("Create Group"):
                try:
                    users_list = [u.strip() for u in initial_users.split('\n') if u.strip()]
                    result = asyncio.run(client.create_group(group_name, users_list))
                    st.success(f"✅ Created group: {group_name}")
                    st.session_state.groups = asyncio.run(fetch_groups())
                except Exception as e:
                    st.error(f"❌ Error creating group: {e}")
    
    # Display groups
    groups = st.session_state.groups or asyncio.run(fetch_groups())
    
    for group in groups:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**{group.get('name')}**")
            
            with col2:
                users_in_group = group.get('users', [])
                st.write(f"👥 {len(users_in_group)} members: {', '.join(users_in_group[:3])}{'...' if len(users_in_group) > 3 else ''}")
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_group_{group['name']}"):
                    try:
                        asyncio.run(client.delete_group(group["name"]))
                        st.success("Group deleted!")
                        st.session_state.groups = asyncio.run(fetch_groups())
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            st.divider()

# Services page
elif page == "Services":
    st.header("🔧 Services")
    
    if st.button("🔄 Refresh Services"):
        st.session_state.services = asyncio.run(fetch_services())
        st.success("Services refreshed!")
    
    services = st.session_state.services or asyncio.run(fetch_services())
    
    for service in services:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                admin_badge = "👑" if service.get("admin") else "🔧"
                st.write(f"{admin_badge} **{service.get('name')}**")
            
            with col2:
                url = service.get("url", "N/A")
                if url != "N/A":
                    st.link_button("🔗 Open", url)
                else:
                    st.write("No URL")
            
            with col3:
                pid = service.get("pid")
                status = "🟢 Running" if pid else "🔴 Stopped"
                st.write(status)
            
            st.divider()

# Admin page
elif page == "Admin":
    st.header("⚙️ Admin Operations")
    
    st.warning("⚠️ Admin operations can affect the entire JupyterHub instance. Use with caution!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧹 Maintenance")
        
        if st.button("🗑️ Cull Idle Servers"):
            try:
                result = asyncio.run(client.cull_servers())
                st.success("✅ Server culling initiated")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        if st.button("🔄 Check Proxy"):
            try:
                proxy_info = asyncio.run(client.get_proxy())
                st.json(proxy_info)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        st.subheader("🚨 Critical Operations")
        
        st.write("**Shutdown Hub**")
        if st.button("🛑 Shutdown JupyterHub", type="primary"):
            if st.checkbox("I understand this will shut down the hub"):
                try:
                    result = asyncio.run(client.shutdown_hub())
                    st.warning("🛑 Hub shutdown initiated!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# Tokens page
elif page == "Tokens":
    st.header("🔐 Token Management")
    
    st.info("Token management for API access")
    
    # Create token form
    with st.expander("➕ Create New Token"):
        with st.form("create_token_form"):
            token_user = st.text_input("Username")
            token_note = st.text_input("Note (optional)")
            expires_in = st.number_input("Expires in (seconds, optional)", min_value=0, value=0)
            
            if st.form_submit_button("Create Token"):
                try:
                    expires = expires_in if expires_in > 0 else None
                    result = asyncio.run(client.create_token(token_user, token_note, expires))
                    st.success("✅ Token created!")
                    st.code(result.get("token", "Token not returned"), language="text")
                except Exception as e:
                    st.error(f"❌ Error creating token: {e}")
    
    # List tokens (admin only)
    if st.button("📝 List All Tokens (Admin)"):
        try:
            tokens = asyncio.run(client.list_tokens())
            if tokens:
                df = pd.DataFrame(tokens)
                st.dataframe(df)
            else:
                st.info("No tokens found")
        except Exception as e:
            st.error(f"❌ Error fetching tokens: {e}")

# Servers page
elif page == "Servers":
    st.header("🖥️ Server Management")
    
    users = asyncio.run(fetch_users())
    
    for user in users:
        servers = user.get("servers", {})
        if servers:
            st.subheader(f"👤 {user['name']}")
            
            for server_name, server_info in servers.items():
                display_name = server_name if server_name else "default"
                
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{display_name}**")
                
                with col2:
                    ready = server_info.get("ready", False)
                    status = "🟢 Ready" if ready else "🟡 Starting"
                    st.write(status)
                
                with col3:
                    if server_info.get("url"):
                        st.link_button("🔗 Access", server_info["url"])
                
                with col4:
                    if st.button("⏹️ Stop", key=f"stop_server_{user['name']}_{server_name}"):
                        try:
                            asyncio.run(client.stop_server(user["name"], server_name))
                            st.success("Server stopping...")
                        except Exception as e:
                            st.error(f"Error: {e}")
            
            st.divider()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🚀 **JupyterHub Manager**")
st.sidebar.markdown("Professional admin interface")
st.sidebar.markdown(f"Built with Streamlit")
