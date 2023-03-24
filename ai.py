# import required libraries
import openai
import streamlit as st


def create_prompt(user_params):
  prompt = f'Please provide itinerary for {user_params["location"]} during the month of {user_params["month"]} for {user_params["days"]} days. We need the following mix of activities {user_params["activities"]}. Suggest us restaurant options based on our interests in {user_params["food"]}'
  return prompt


def create_image_prompt(user_params):
  image_prompt = f'beautiful {user_params["location"]} during the month of {user_params["month"]}.'
  return image_prompt


def get_data_from_openai(prompt):
  # User GPT-3 to generate a summary of the article
  response = openai.Completion.create(
      engine = "text-davinci-003",
      prompt = prompt,
      max_tokens = 2000,
      temperature = 0.3 
    )
  # print the summary generated
  response = response['choices'][0]['text']
  return response

def generate_image(prompt):
  response = openai.Image.create(
     prompt=prompt, 
     n=1, 
     size="512x512"
     )
  image_url = response['data'][0]['url']
  return image_url


def construct_sidebar_form():
  st.header('Travel Itinerary App Using OpenAI + Streamlit')
  user_params = {}
  with st.sidebar.form('Home Purchase Calculator Form'):
    with st.expander("Location", expanded=True):
      user_params['location'] = st.text_input('Place to visit?')
      user_params['days'] = st.number_input('Number of days?')
      user_params['month'] = st.text_input('Which month?')
      user_params['activities'] = st.multiselect("Select activities you'd like to do:", 
                                  ['Hiking', 'Off the beaten path', 'Museum and Arts', 'Science', 'Adventure', 
                                                          'Kid Friendly'])
      user_params['food'] = st.multiselect("For restaurant recommendation, select food you'd like to eat:", ['Vegetarian', 'Thai', 'American', 'Italian'])
    submitted = st.form_submit_button('Generate Itinerary')
    return submitted, user_params


def main():
  
  #read the openai api key from secrets.toml
  openai.api_key = st.secrets['gpt_key']
  submitted, user_params = construct_sidebar_form()
  
  if submitted:
    prompt = create_prompt(user_params=user_params)
    response = get_data_from_openai(prompt=prompt)
    image_prompt = create_image_prompt(user_params=user_params)
    image = generate_image(prompt=image_prompt)
    st.info(response)   
    st.download_button('Download', response)
    st.image(image)

if __name__ == "__main__":
    main()
