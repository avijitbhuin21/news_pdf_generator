style = """/* A simple CSS reset and basic styling */
        body {
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #F0EEE9; /* A slightly darker background to make the content pop */
            color: #3D3D3D;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }

        /* The main container for the content */
        .card-container {
            background-color: #F8F6F2; /* The off-white color from the image */
            padding: 24px;
            max-width: 600px;
            width: 100%;
            box-sizing: border-box;
            border: 1px solid #EAE8E3;
            border-radius: 8px; /* Subtle rounded corners for the container */
        }

        /* Header section with profile pic and username */
        .post-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }

        .profile-pic {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover; /* Ensures the image covers the area without distortion */
        }

        .username {
            font-size: 1rem;
            font-weight: 500;
        }

        /* The main image of the post */
        .main-image {
            width: 100%;
            height: auto;
            border-radius: 12px;
            display: block; /* Removes any extra space below the image */
        }

        /* The content of the post */
        .post-content {
            margin-top: 24px;
        }

        h1 {
            font-size: 1.6rem;
            font-weight: 700;
            text-transform: uppercase;
            line-height: 1.3;
            margin: 0 0 20px 0;
        }

        p {
            font-size: 1.1rem;
            line-height: 1.6;
            margin: 0 0 1.2em 0;
        }

        /* Styling for the link at the bottom */
        .learn-more-link {
            color: #3D3D3D;
            text-decoration: underline;
            font-size: 1rem;
        }
        
        .learn-more-link:hover {
            color: #000;
        }"""



def get_html_content(data:dict):
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIT Study on ChatGPT</title>
    <style>
    {style}
    </style>
</head>
<body>

    <div class="card-container">
        <header class="post-header">
            <img class="profile-pic" src="https://picsum.photos/id/237/40/40" alt="Profile picture of Rakesh Gohel">
            <span class="username">@username</span>
        </header>

        <img class="main-image" src="{data['media_url']}" alt="Abstract tech-related image">

        <div class="post-content">
            <h1>{data['title'].upper()}</h1>
            
            <p>Major finding:</p>
            
            <p>
                {data['description']}
            </p>
            

            <a href="{data['link']}" class="learn-more-link">Click here to learn more</a>
        </div>
    </div>

</body>
</html>"""
    return template