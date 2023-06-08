from bs4 import BeautifulSoup, Comment
import cssutils

def analyze_html(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'lxml')

    tags = [tag for tag in soup.find_all(True)]

    tag_counts = {tag.name: len(soup.find_all(tag.name)) for tag in tags}

    tag_lengths = {tag.name: len(tag.string) if tag.string else 0 for tag in tags}

    avg_tag_length = sum(tag_lengths.values()) / len(tag_lengths) if len(tag_lengths) > 0 else 0

    ids = sum(1 for tag in tags if tag.get('id'))
    classes = sum(1 for tag in tags if tag.get('class'))

    styles = [tag.get('style') for tag in tags if tag.get('style')]
    num_inline_styles = len(styles)
    avg_num_rules_per_style = sum(len(cssutils.parseStyle(style).keys()) for style in styles) / num_inline_styles if num_inline_styles > 0 else 0

    comments = sum(1 for element in soup.recursiveChildGenerator() if isinstance(element, Comment))

    return {
        'tag_counts': tag_counts,
        'avg_tag_length': avg_tag_length,
        'num_ids': ids,
        'num_classes': classes,
        'num_inline_styles': num_inline_styles,
        'avg_num_rules_per_style': avg_num_rules_per_style,
        'num_comments': comments,
    }

stats = analyze_html('desktop/physics.html')

for key, value in stats.items():
    print(f'{key}: {value}')