import urllib.request
import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from collections import Counter
from typing import Dict, List, Set
import logging
import time
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='gutenberg_analysis.log'
)

@dataclass
class BookPerformanceMetrics:
    title: str
    start_time: float
    end_time: float
    processing_time: float
    success: bool
    error_message: str = ""

class Visualizer:
    def __init__(self, output_dir: str = 'visualizations'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Try to set a simple, reliable style
            plt.style.use('classic')  # Using 'classic' style which is always available
            
            # Configure color palette manually
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
            
        except Exception as e:
            logging.warning(f"Could not set matplotlib style: {str(e)}. Using default style.")

    def create_frequency_bar_chart(self, frequencies: Dict[str, int], title: str):
        """Create a bar chart of the top 20 proper nouns and their frequencies."""
        try:
            # Sort frequencies and get top 20
            sorted_items = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:20]
            nouns, counts = zip(*sorted_items)

            # Create figure with larger size for better readability
            plt.figure(figsize=(15, 8))
            
            # Create bar plot with custom colors
            bars = plt.bar(range(len(nouns)), counts, color='#1f77b4')
            
            # Customize the plot
            plt.title(f'Top 20 Proper Nouns in {title}', fontsize=14, pad=20)
            plt.xlabel('Proper Nouns', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            
            # Rotate x-axis labels for better readability
            plt.xticks(range(len(nouns)), nouns, rotation=45, ha='right')
            
            # Add value labels on top of each bar
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom')
            
            # Adjust layout to prevent label cutoff
            plt.tight_layout()
            
            # Save the plot
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.output_dir}/{title.replace(' ', '_')}_top20_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
            
        except Exception as e:
            logging.error(f"Error creating visualization for {title}: {str(e)}")
            return None

class PerformanceTracker:
    def __init__(self):
        self.start_time = time.time()
        self.book_metrics: List[BookPerformanceMetrics] = []
        
    def add_book_metric(self, metric: BookPerformanceMetrics):
        self.book_metrics.append(metric)
        
    def generate_performance_report(self, output_dir: str = 'reports'):
        """Generate a detailed performance report."""
        end_time = time.time()
        total_runtime = end_time - self.start_time
        
        # Calculate statistics
        successful_books = [m for m in self.book_metrics if m.success]
        success_rate = len(successful_books) / len(self.book_metrics) if self.book_metrics else 0
        
        processing_times = [m.processing_time for m in successful_books]
        avg_time_per_book = sum(processing_times) / len(processing_times) if processing_times else 0
        
        report = {
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'total_runtime_seconds': round(total_runtime, 2),
            'total_books_attempted': len(self.book_metrics),
            'successful_books': len(successful_books),
            'success_rate': f"{success_rate:.2%}",
            'average_time_per_book': round(avg_time_per_book, 2),
            'performance_metrics': {
                'fastest_book': min(processing_times) if processing_times else 0,
                'slowest_book': max(processing_times) if processing_times else 0,
                'total_processing_time': sum(processing_times)
            },
            'book_details': [
                {
                    'title': m.title,
                    'processing_time': round(m.processing_time, 2),
                    'success': m.success,
                    'error_message': m.error_message
                }
                for m in self.book_metrics
            ]
        }
        
        # Save report
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/performance_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return report

class GutenbergAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
            nltk.download('maxent_ne_chunker')
            nltk.download('words')
        except Exception as e:
            logging.error(f"Failed to download NLTK data: {str(e)}")
            raise

        self.books_data = {}
        self.total_frequencies = Counter()
        self.visualizer = Visualizer()
        self.performance_tracker = PerformanceTracker()
        
    def fetch_book_text(self, url: str) -> str:
        """Retrieve book text from Project Gutenberg URL."""
        try:
            with urllib.request.urlopen(url) as response:
                text = response.read().decode('utf-8')
                
            # Remove Project Gutenberg header and footer
            start_marker = "*** START OF THIS PROJECT GUTENBERG"
            end_marker = "*** END OF THIS PROJECT GUTENBERG"
            
            start_idx = text.find(start_marker)
            if start_idx != -1:
                start_idx = text.find("\n", start_idx) + 1
            else:
                start_idx = 0
                
            end_idx = text.find(end_marker)
            if end_idx == -1:
                end_idx = len(text)
                
            return text[start_idx:end_idx].strip()
            
        except Exception as e:
            logging.error(f"Error fetching book from {url}: {str(e)}")
            return ""

    def extract_proper_nouns(self, text: str) -> List[str]:
        """Extract proper nouns from text using NLTK."""
        proper_nouns = []
        
        try:
            # Tokenize and tag the text
            sentences = sent_tokenize(text)
            for sentence in sentences:
                tokens = word_tokenize(sentence)
                tagged = pos_tag(tokens)
                named_entities = ne_chunk(tagged)
                
                # Extract named entities
                for chunk in named_entities:
                    if hasattr(chunk, 'label'):
                        entity_name = ' '.join(c[0] for c in chunk.leaves())
                        proper_nouns.append(entity_name)
                        
        except Exception as e:
            logging.error(f"Error extracting proper nouns: {str(e)}")
            
        return proper_nouns

    def analyze_book(self, url: str, title: str):
        """Analyze a single book and update frequencies."""
        start_time = time.time()
        success = False
        error_message = ""
        
        try:
            # Fetch and process the book
            text = self.fetch_book_text(url)
            if not text:
                error_message = f"Failed to fetch text for {title}"
                raise Exception(error_message)
                
            proper_nouns = self.extract_proper_nouns(text)
            frequencies = Counter(proper_nouns)
            
            # Store individual book results
            self.books_data[title] = {
                'url': url,
                'frequencies': frequencies,
                'total_proper_nouns': len(proper_nouns),
                'unique_proper_nouns': len(set(proper_nouns))
            }
            
            # Update total frequencies
            self.total_frequencies.update(proper_nouns)
            
            # Create visualization for this book
            self.visualizer.create_frequency_bar_chart(
                dict(frequencies.most_common(20)),
                title
            )
            
            success = True
            
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error analyzing book {title}: {error_message}")
            
        finally:
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Track performance metrics
            self.performance_tracker.add_book_metric(
                BookPerformanceMetrics(
                    title=title,
                    start_time=start_time,
                    end_time=end_time,
                    processing_time=processing_time,
                    success=success,
                    error_message=error_message
                )
            )

    def generate_reports(self, output_dir: str = 'reports'):
        """Generate JSON reports and performance metrics."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate individual book reports
            for title, data in self.books_data.items():
                report = {
                    'title': title,
                    'url': data['url'],
                    'statistics': {
                        'total_proper_nouns': data['total_proper_nouns'],
                        'unique_proper_nouns': data['unique_proper_nouns']
                    },
                    'frequencies': dict(data['frequencies'].most_common())
                }
                
                filename = f"{output_dir}/{title.replace(' ', '_')}_report.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Create visualization for combined frequencies
            self.visualizer.create_frequency_bar_chart(
                dict(self.total_frequencies.most_common(20)),
                "Combined Books"
            )
            
            # Generate performance report
            performance_report = self.performance_tracker.generate_performance_report(output_dir)
            
            # Generate combined report with performance metrics
            combined_report = {
                'total_books_analyzed': len(self.books_data),
                'total_frequencies': dict(self.total_frequencies.most_common()),
                'books_analyzed': list(self.books_data.keys()),
                'performance_metrics': performance_report
            }
            
            with open(f"{output_dir}/combined_report.json", 'w', encoding='utf-8') as f:
                json.dump(combined_report, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"Error generating reports: {str(e)}")