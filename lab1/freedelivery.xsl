<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<body>
  <table border="1">
    <tr>
      <th style="text-align:center">Image</th>
      <th style="text-align:center">Text</th>
      <th style="text-align:center">Price</th>
    </tr>
    <xsl:for-each select="data/item">
    <tr>
      <td><img src="{image}"/></td>
      <td><xsl:value-of select="text"/></td>
      <td><xsl:value-of select="price"/></td>
    </tr>
    </xsl:for-each>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
