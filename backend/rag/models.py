from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    content = models.TextField(blank=True)
    source = models.CharField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks",
    )
    content = models.TextField()
    chunk_index = models.PositiveIntegerField()
    token_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["document", "chunk_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "chunk_index"],
                name="unique_document_chunk",
            )
        ]

    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"


class DocumentEmbedding(models.Model):
    chunk = models.OneToOneField(
        DocumentChunk,
        on_delete=models.CASCADE,
        related_name="embedding",
    )
    embedding = models.JSONField()
    model_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding - {self.chunk}"


class RAGQuery(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True)
    retrieved_chunks = models.JSONField(
        default=list,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question[:100]
