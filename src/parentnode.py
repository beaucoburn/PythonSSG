from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        # Get attributes string
        attrs = self.props_to_html()
        
        # Recursively render all children
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{attrs}>{children_html}</{self.tag}>"
