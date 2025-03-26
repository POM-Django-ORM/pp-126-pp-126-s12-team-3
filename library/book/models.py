from django.db import models

class Book(models.Model):
    
    # This class represents a Book.
    # Attributes:
    # -----------
    # param name: Describes name of the book
    # param description: Describes description of the book
    # param count: Describes count of the book
    # param authors: list of Authors
    

    name = models.CharField(max_length=128)  # Назва книги
    description = models.TextField(default="Default description")  # Опис книги
    count = models.IntegerField(default=10)  # Кількість книг
    authors = models.ManyToManyField('author.Author', blank=True)  # Зв’язок з авторами

    def __str__(self):
        return f"'id': {self.id}, 'name': '{self.name}', 'description': '{self.description}', 'count': {self.count}, 'authors': {[author.id for author in self.authors.all()]}"

    def __repr__(self):
        return f"Book(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        book = Book.get_by_id(book_id)
        if book:
            book.delete()
            return True
        return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        if len(name) > 128:
            return None
        book = Book(name=name, description=description, count=count)
        book.save()
        if authors:
            book.authors.set(authors)
        return book

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.id for author in self.authors.all()]
        }

    def update(self, name=None, description=None, count=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        self.authors.add(*authors)

    def remove_authors(self, authors):
        self.authors.remove(*authors)

    @staticmethod
    def get_all():
        return list(Book.objects.all())
