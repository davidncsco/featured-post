import streamlit as st
from bs4 import BeautifulSoup

td_element_template = """
     <td>
        <a href="%s">
            <img src="%s" class="featured-image">
        </a>
        <p>
            <a href="%s">%s</a>
        </p>
     </td>
"""

def extract_text_between_markers(text, start_marker, end_marker):
    """
    Extracts the text between two markers in a text file.

    Args:
        text: content of the text to extract
        start_marker: The string marking the beginning of the text to extract.
        end_marker: The string marking the end of the text to extract.

    Returns:
        Tuple with the extracted texts, or an empty string if no text is found between the markers.
    """
    start_index = text.find(start_marker) + len(start_marker)
    end_index = text.find(end_marker)

    if start_index != -1 and end_index != -1:
        return (text[:start_index],text[start_index:end_index],text[end_index:])
    else:
        return ()
    
def strip_after_image_size(url):
    # Find the index of 'image-size' substring (or -1 if not found)
    index = url.find("image-size")

    # If 'image-size' is found, strip the url from that index onwards
    if index != -1:
        stripped_url = url[:index]
    else:
        stripped_url = url

    return stripped_url

def add_utm_source(url):
    # add 'utm_source=devhubportal' to post url if not present
    if url.find("utm_source=devhubportal") == -1:
        return f"{url}?utm_source=devhubportal"
    return url

st.title("DevNet Hub Feature Posts Banner")
st.write("")
post_url = st.text_input("Enter post URL")
thumb_url = st.text_input("Enter thumbnail URL")
display_text = st.text_input("Enter display text")

url = "https://community.cisco.com/t5/bizapps/bizappspage/tab/community%3Aadmin%3Acontent/node-display-id/category%3A4409j-developer-home"
st.write("Click on this [link](%s) to go to the Featured Content admin page" % url)
current_banner = st.text_area("Cut and paste HTML content for current banner in \"Welcome/Featured Content Text\"",value="",height=50)

button1 = st.button("Generate new banner")


if button1 and len(current_banner) > 0:
     
    start_marker = "<!-- Edit below -->"
    end_marker = "<!-- Edit above -->"

    extracted_text = extract_text_between_markers(current_banner, start_marker, end_marker)
    generated_text = extracted_text[0]
    
    if len(extracted_text) > 0:
        post_url = add_utm_source(post_url)
        td_element = td_element_template % (post_url,strip_after_image_size(thumb_url),post_url,display_text)
        generated_text = f"{generated_text}{td_element}"
        
        soup = BeautifulSoup(extracted_text[1], 'html.parser')

        # Get all <td> elements
        td_elements = soup.find_all('td')
        # Extract text content
        for cell in td_elements[:2]:
            # Extract image source (if present)
            image_element = cell.find('img')
            link_element = cell.find('a')
            paragraphs = cell.find_all('p')
        
            if image_element and link_element and paragraphs:    # all elements must be present
                image_src = image_element['src']
                link_url = link_element['href']
                for paragraph in paragraphs:
                    text = paragraph.get_text()
                    break
                td_element = td_element_template % (link_url,strip_after_image_size(image_src),link_url,text)
                generated_text = f"{generated_text}{td_element}"
        generated_text = f"{generated_text}{extracted_text[2]}"
        st.code(generated_text)
    else:
        print("No text found between markers.")
