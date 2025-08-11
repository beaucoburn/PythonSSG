class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by child classes")

    def props_to_html(self):
        if not self.props:
            return ""
        
        attrs = []
        for key, value in self.props.items():
            attrs.append(f'{key}="{value}"')
        
        return " " + " ".join(attrs)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
