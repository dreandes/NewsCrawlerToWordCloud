from itemadapter import ItemAdapter
from .mongodb import collection

class NewsdaumPipeline:
    
    def process_item(self, item, spider):
        
        data = {
            "title": item["title"],
            "category": item["category"],
            "content": item["content"],
            "link": item["link"],
        }
        collection.insert(data)
        
        return item
