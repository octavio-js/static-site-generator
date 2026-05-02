class HTMLNode:
  def __init__(self, tag = None, value = None, children = None, props = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError()

  def props_to_html(self):
    if not self.props:
      return ""

    properties = " "
    for key, value in self.props.items():
      properties += f'{key}="{value}" '

    return properties.rstrip()

  def __repr__(self):
    return f'<{self.tag}{self.props_to_html()}>{self.value} / {self.children}</{self.tag}>'

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props = None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if not self.value:
      raise ValueError("All leaf nodes must have a value")

    if not self.tag:
      return self.value

    properties = super().props_to_html()
    return f'<{self.tag}{properties}>{self.value}</{self.tag}>'

  def __repr__(self):
    return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
