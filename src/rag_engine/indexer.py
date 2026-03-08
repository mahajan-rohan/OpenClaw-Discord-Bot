import time
from src.rag_engine.vector_store import VectorStore

class RAGController:
    def __init__(self):
        print("⏳ RAG Controller: Loading AI Model into Memory (GPU)...")
        self.vector_store = VectorStore()
        
        # Warm up the engine to prevent first-run lag
        try:
            self.vector_store.collection.query(query_texts=["warmup"], n_results=1)
            print("✅ AI Model Loaded & Ready.")
        except Exception:
            print("✅ AI Model Loaded.")

    def index_message(self, message):
        """
        Splits a Discord message into facts and saves them to Vector DB.
        """
        # Ignore empty messages or system messages
        if not message.content or message.author.bot:
            return

        metadata = {
            "author": message.author.name,
            "channel": message.channel.name if hasattr(message.channel, 'name') else "DM",
            "timestamp": message.created_at.timestamp()
        }
        
        # SPLIT MULTI-LINE MESSAGES
        # This ensures "I love Java" and "I live in IITKGP" become separate memories.
        content_lines = message.content.split('\n')
        
        for line in content_lines:
            clean_line = line.strip()
            # Ignore short garbage
            if len(clean_line) < 5: 
                continue
                
            print(f"📥 Indexing Fact: '{clean_line[:30]}...'")
            self.vector_store.add_memory(text=clean_line, metadata=metadata)

    def retrieve_context(self, queries, threshold=1.8) -> str:
        """
        Searches memory using MULTIPLE query variations.
        
        Args:
            queries: A list of strings (e.g. ["where do i live", "my address"])
            threshold: Distance score cutoff. Lower is stricter. 
                       1.8 is forgiving enough to match 'live' with 'stay'.
        """
        # Ensure input is a list, even if a single string is passed
        if isinstance(queries, str):
            queries = [queries]

        all_memories = set()
        print(f"🔍 Searching Vector DB for {len(queries)} variations...")
        
        for q in queries:
            # Get results for this variation
            # We ask for distance scores to filter bad matches
            results_with_scores = self.vector_store.search(q, n_results=3)
            
            if not results_with_scores:
                continue
            
            for text, score in results_with_scores:
                # DEBUG: Print matches to terminal
                if score < threshold:
                    print(f"   MATCH! Query: '{q}' found -> '{text[:20]}...' (Score: {round(score, 3)})")
                    
                    # FILTER: Garbage Collection
                    # 1. Ignore questions (we don't want to remember us asking)
                    if "?" in text: 
                        continue
                    # 2. Ignore mentions/chat logs
                    if text.strip().startswith("<@") or text.strip().startswith("@"):
                        continue
                        
                    all_memories.add(text)

        if not all_memories:
            return "No relevant past memories found."
            
        # Return unique memories joined by newlines
        return "\n".join([f"- {m}" for m in all_memories])