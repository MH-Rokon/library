from django.http import HttpResponse

def home_view(request):
    # Determine base URL dynamically from the request
    host = request.get_host()  # e.g. "localhost:8000" or "library-uniy.onrender.com"
    if "localhost" in host or "127.0.0.1" in host:
        base_url = "http://localhost:8000"
    else:
        base_url = "https://library-uniy.onrender.com"

    html_content = f"""
    <html>
        <head>
            <title>Library Management API Home</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 40px;
                    color: #333;
                }}
                h1 {{
                    color: #2980b9;
                }}
                .section {{
                    margin-top: 30px;
                }}
                .endpoint {{
                    margin-left: 20px;
                    color: #2c3e50;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <h1>Welcome to the Library Management API</h1>
            <p>Click on the links below to navigate the API endpoints</p>

            <div class="section">
                <h2>Authentication</h2>
                <div class="endpoint"><a href="{base_url}/api/register/">Register</a></div>
                <div class="endpoint"><a href="{base_url}/api/activate/&lt;uidb64&gt;/&lt;token&gt;/">Activate Account</a></div>
                <div class="endpoint"><a href="{base_url}/api/login/">Login</a></div>
                <div class="endpoint"><a href="{base_url}/api/logout/">Logout</a></div>
                <div class="endpoint"><a href="{base_url}/api/reset-password-request/">Password Reset Request</a></div>
                <div class="endpoint"><a href="{base_url}/api/reset-password-confirm/&lt;uidb64&gt;/&lt;token&gt;/">Password Reset Confirm</a></div>
                <div class="endpoint"><a href="{base_url}/api/profile/">User Profile</a></div>
            </div>

            <div class="section">
                <h2>Library (Books, Authors, Categories)</h2>
                <div class="endpoint"><a href="{base_url}/library/authors/">Authors</a></div>
                <div class="endpoint"><a href="{base_url}/library/categories/">Categories</a></div>
                <div class="endpoint"><a href="{base_url}/library/books/">Books</a></div>
                <div class="endpoint"><a href="{base_url}/library/books/create/">Add Book (Admin only)</a></div>
                <div class="endpoint"><a href="{base_url}/library/books/&lt;id&gt;/update/">Update Book (Admin only)</a></div>
                <div class="endpoint"><a href="{base_url}/library/books/&lt;id&gt;/delete/">Delete Book (Admin only)</a></div>
            </div>

            <div class="section">
                <h2>Borrowing</h2>
                <div class="endpoint"><a href="{base_url}/borrow/book/">Borrow a Book</a></div>
                <div class="endpoint"><a href="{base_url}/borrow/book/list/">List My Borrows</a></div>
                <div class="endpoint"><a href="{base_url}/borrow/return/">Return a Book</a></div>
                <div class="endpoint"><a href="{base_url}/borrow/users/&lt;id&gt;/penalties/">User Penalty Points</a></div>
            </div>

            <div class="section">
                <h2>JWT Authentication</h2>
                <div class="endpoint"><a href="{base_url}/api/token/">Get Token</a></div>
                <div class="endpoint"><a href="{base_url}/api/token/refresh/">Refresh Token</a></div>
            </div>
        </body>
    </html>
    """

    return HttpResponse(html_content)
