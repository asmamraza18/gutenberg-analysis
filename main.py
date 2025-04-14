from gutenberg_analyzer import GutenbergAnalyzer
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='gutenberg_analysis.log'
)

# Sample list of Project Gutenberg books
BOOKS_TO_ANALYZE = [
    {'url': 'https://www.gutenberg.org/files/1342/1342-0.txt', 'title': 'Pride and Prejudice'},
    {'url': 'https://www.gutenberg.org/files/84/84-0.txt', 'title': 'Frankenstein'},
    {'url': 'https://www.gutenberg.org/files/11/11-0.txt', 'title': 'Alice’s Adventures in Wonderland'},
    {'url': 'https://www.gutenberg.org/files/1661/1661-0.txt', 'title': 'The Adventures of Sherlock Holmes'},
    {'url': 'https://www.gutenberg.org/files/2701/2701-0.txt', 'title': 'Moby Dick'},
    {'url': 'https://www.gutenberg.org/files/345/345-0.txt', 'title': 'Dracula'},
    {'url': 'https://www.gutenberg.org/files/98/98-0.txt', 'title': 'A Tale of Two Cities'},
    {'url': 'https://www.gutenberg.org/files/74/74-0.txt', 'title': 'The Adventures of Tom Sawyer'},
    {'url': 'https://www.gutenberg.org/files/120/120-0.txt', 'title': 'Treasure Island'},
    {'url': 'https://www.gutenberg.org/files/1952/1952-0.txt', 'title': 'The Yellow Wallpaper'},
    {'url': 'https://www.gutenberg.org/files/55/55-0.txt', 'title': 'The Wonderful Wizard of Oz'},
    {'url': 'https://www.gutenberg.org/files/1080/1080-0.txt', 'title': 'A Modest Proposal'},
    {'url': 'https://www.gutenberg.org/files/2600/2600-0.txt', 'title': 'War and Peace'},
    {'url': 'https://www.gutenberg.org/files/5200/5200-0.txt', 'title': 'Metamorphosis'},
    {'url': 'https://www.gutenberg.org/files/4300/4300-0.txt', 'title': 'Ulysses'},
    {'url': 'https://www.gutenberg.org/files/1344/1344-0.txt', 'title': 'The Secrets Of The Princesse De Cadignan'},
    {'url': 'https://www.gutenberg.org/files/1400/1400-0.txt', 'title': 'Great Expectations'},
    {'url': 'https://www.gutenberg.org/files/16/16-0.txt', 'title': 'Peter Pan'},
    {'url': 'https://www.gutenberg.org/files/34580/34580-0.txt', 'title': 'The Ego And His Own'},
    {'url': 'https://www.gutenberg.org/files/829/829-0.txt', 'title': 'Gulliver’s Travels'},
    {'url': 'https://www.gutenberg.org/files/6130/6130-0.txt', 'title': 'The Iliad'},
    {'url': 'https://www.gutenberg.org/files/1497/1497-0.txt', 'title': 'The Republic'},
    {'url': 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt', 'title': 'Romeo and Juliet'},
    {'url': 'https://www.gutenberg.org/files/158/158-0.txt', 'title': 'Emma'},
    {'url': 'https://www.gutenberg.org/cache/epub/2554/pg2554.txt', 'title': 'Crime and Punishment'},
    {'url': 'https://www.gutenberg.org/files/25344/25344-0.txt', 'title': 'The Scarlet Letter'},
    {'url': 'https://www.gutenberg.org/files/219/219-0.txt', 'title': 'Heart of Darkness'},
    {'url': 'https://www.gutenberg.org/files/42/42-0.txt', 'title': 'The Strange Case of Dr. Jekyll and Mr. Hyde'},
    {'url': 'https://www.gutenberg.org/files/36/36-0.txt', 'title': 'The War of the Worlds'},
    {'url': 'https://www.gutenberg.org/files/160/160-0.txt', 'title': 'The Awakening'},
    {'url': 'https://www.gutenberg.org/files/159/159-0.txt', 'title': 'The Island of Doctor Moreau'},
    {'url': 'https://www.gutenberg.org/files/1260/1260-0.txt', 'title': 'Jane Eyre'},
    {'url': 'https://www.gutenberg.org/files/768/768-0.txt', 'title': 'Wuthering Heights'},
    {'url': 'https://www.gutenberg.org/files/161/161-0.txt', 'title': 'Sense and Sensibility'},
    {'url': 'https://www.gutenberg.org/files/2814/2814-0.txt', 'title': 'Dubliners'},
    {'url': 'https://www.gutenberg.org/files/30254/30254-0.txt', 'title': 'The Romance of Lust'},
    {'url': 'https://www.gutenberg.org/files/766/766-0.txt', 'title': 'David Copperfield'},
    {'url': 'https://www.gutenberg.org/files/16389/16389-0.txt', 'title': 'The Enchanted April'},
    {'url': 'https://www.gutenberg.org/cache/epub/1232/pg1232.txt', 'title': 'The Prince'},
    {'url': 'https://www.gutenberg.org/files/3296/3296-0.txt', 'title': 'The Confessions of St. Augustine'},
    {'url': 'https://www.gutenberg.org/files/204/204-0.txt', 'title': 'The Innocence of Father Brown'},
    {'url': 'https://www.gutenberg.org/files/8800/8800-0.txt', 'title': 'The Divine Comedy'},
    {'url': 'https://www.gutenberg.org/files/42108/42108-0.txt', 'title': 'The Federalist Papers'},
    {'url': 'https://www.gutenberg.org/files/2500/2500-0.txt', 'title': 'Siddhartha'},
    {'url': 'https://www.gutenberg.org/files/132/132-0.txt', 'title': 'The Art of War'},
    {'url': 'https://www.gutenberg.org/files/2000/2000-0.txt', 'title': 'Don Quijote'},
    {'url': 'https://www.gutenberg.org/files/28054/28054-0.txt', 'title': 'The Brothers Karamazov'},
    {'url': 'https://www.gutenberg.org/cache/epub/36034/pg36034.txt', 'title': 'White Nights and Other Stories'},
    {'url': 'https://www.gutenberg.org/files/514/514-0.txt', 'title': 'Little Women'},
    {'url': 'https://www.gutenberg.org/files/2542/2542-0.txt', 'title': 'A Doll’s House'},
]


def main():
    start_time = time.time()
    logging.info("Starting Gutenberg text analysis...")
    
    analyzer = GutenbergAnalyzer()
    
    # Process each book
    for book in BOOKS_TO_ANALYZE:
        logging.info(f"Processing book: {book['title']}")
        analyzer.analyze_book(book['url'], book['title'])
        
    # Generate reports
    logging.info("Generating reports...")
    analyzer.generate_reports()
    
    end_time = time.time()
    logging.info(f"Analysis completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()