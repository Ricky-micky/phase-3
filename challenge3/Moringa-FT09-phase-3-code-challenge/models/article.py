import sqlite3
def get_db_connection():
    conn = sqlite3.connect(':memory:')  
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE magazines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors (id),
            FOREIGN KEY (magazine_id) REFERENCES magazines (id)
        )
    ''')
    cursor.execute("INSERT INTO authors (id, name) VALUES (1, 'Alice Smith')")
    cursor.execute("INSERT INTO magazines (id, name, category) VALUES (1, 'Tech World', 'Technology')")
    conn.commit()

    return conn

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.name}>"

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.name}>"

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):  
        if not all([id, title, content, author_id, magazine_id]):
            raise ValueError("All fields (id, title, content, author_id, magazine_id) are required.")
        
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self): 
        return f"<Article {self.title}>"

    @property
    def author(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
            author_data = cursor.fetchone()
        
        if author_data:
            return Author(author_data['id'], author_data['name'])
        return None

    @property
    def magazine(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
            magazine_data = cursor.fetchone()
        
        if magazine_data:
            return Magazine(magazine_data['id'], magazine_data['name'], magazine_data['category'])
        return None


# Test the code
article = Article(1, "AI Revolution", "Exploring the future of AI.", 1, 1)
print(article)

# Retrieve the author
print("Author:", article.author)

# Retrieve the magazine
print("Magazine:", article.magazine)
