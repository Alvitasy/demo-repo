import streamlit as st
import requests
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Athena.7t Careers", layout="wide")

# ✅ Display the logo properly using st.image
#st.image("assets/seven_tablets_logo.jpeg")

# ✅ Render the rest of the styled header without the <img> tag
components.html("""
<div style="background-color: #6492cd; width: 100%; padding: 40px 40px 30px 40px; box-sizing: border-box;">

  <div style="display: flex; justify-content: space-between; align-items: center;">

    <!-- Left: Logo -->
    <div style="flex: 1; display: flex; align-items: center;">
      <img src="https://raw.githubusercontent.com/alvitasy/demo-repo/main/seven_tablets_logo.jpeg"
           style="height: 100px; margin-right: 20px;">
    </div>

    <!-- Center: Title -->
    <div style="flex: 2; text-align: center;">
      <h2 style="color: white; margin: 0; font-size: 32px;">7t</h2>
      <h4 style="color: white; margin: 5px 0 0 0; font-size: 20px;">Career Page</h4>
    </div>

    <!-- Right: Navigation Buttons -->
    <div style="flex: 1; display: flex; justify-content: flex-end;">
      <button style="padding: 10px 20px; margin-right: 10px;
                     background-color: white; color: #2596be;
                     border: none; border-radius: 5px;">Home</button>
      <button style="padding: 10px 20px;
                     background-color: white; color: #2596be;
                     border: none; border-radius: 5px;">Login</button>
    </div>

  </div>

</div>
""", height=240)

st.markdown("<div style='margin-top: -60px;'></div>",unsafe_allow_html=True,)

# --- Job Form Section ---
st.markdown("### Post a Job", unsafe_allow_html=True)

with st.form("job_form", clear_on_submit=False):
    col1, col2 = st.columns(2)

    with col1:
        job_title = st.text_input("Job Title")
        custom_note = st.text_input("Custom Note (e.g., US Citizens only)")

    with col2:
        key_focus = st.text_area("Key Skills (comma-separated, e.g., Python, ML, SQL)")

    st.markdown("#### Select Benefits")

    predefined_benefits = [
        "Medical Insurance", "Vision Insurance", "Dental Insurance",
        "401(k)", "Paid Time Off", "Remote Flexibility", "Gym Membership"
    ]

    selected_benefits = st.multiselect("Select any predefined benefits:", predefined_benefits)

    custom_benefits = st.text_input("Add custom benefits (comma-separated):",
                                    placeholder="e.g., Stock options, Pet insurance")

    # Combine benefits
    all_benefits = selected_benefits.copy()
    if custom_benefits:
        all_benefits.extend([b.strip() for b in custom_benefits.split(",") if b.strip()])
    benefits = ", ".join(all_benefits)

    submitted = st.form_submit_button("Generate Job Description")

    if submitted:
        if not job_title or not custom_note or not key_focus or not benefits:
            st.warning("Please fill in all fields before posting.")
        else:
            with st.spinner("Generating job description..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/generate-job-description",
                        json={
                            "job_title": job_title,
                            "custom_note": custom_note,
                            "key_focus": key_focus,
                            "benefits": benefits
                        }
                    )
                    if response.status_code == 200:
                        result = response.json()["job_description"]
                        st.success("Job Description Generated!")
                        st.markdown("---")
                        st.subheader("Job Description Output")
                        st.markdown(result)
                    else:
                        st.error("Error: Backend failed to generate.")
                except Exception as e:
                    st.error(f"Request failed: {e}")
