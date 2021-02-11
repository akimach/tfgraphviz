import time
from IPython.display import HTML

def jupyter_show_as_svg(g):
    """
    Shows object as SVG (by default it is rendered as image).
    @param  g: digraph object
    """
    return HTML(g.pipe(format='svg').decode("utf-8"))

def jupyter_pan_and_zoom(
    g,
    element_styles="height:auto",
    container_styles="overflow:hidden",
    pan_zoom_json = "{controlIconsEnabled: true, zoomScaleSensitivity: 0.4, minZoom: 0.2}"):
    """
    Embeds SVG object into Jupyter cell with ability to pan and zoom.
    @param  g: digraph object
    @param  element_styles: CSS styles for embedded SVG element.
    @param  container_styles: CSS styles for container div element.
    @param  pan_zoom_json: pan and zoom settings, see https://github.com/ariutta/svg-pan-zoom
    """
    svg_txt = g.pipe(format='svg').decode("utf-8")
    html_container_class_name = F"svg_container_{int(time.time())}"
    html = F'''
        <div class="{html_container_class_name}">
            <style>
                .{html_container_class_name} {{
                    {container_styles}
                }}
                .{html_container_class_name} SVG {{
                    {element_styles}
                }}
            </style>
            <script src="https://ariutta.github.io/svg-pan-zoom/dist/svg-pan-zoom.min.js"></script>
            <script type="text/javascript">
                attempts = 5;
                var existCondition = setInterval(function() {{
                  console.log(attempts);
                  svg_el = document.querySelector(".{html_container_class_name} svg");
                  if (svg_el != null) {{
                      console.log("Exists!");
                      clearInterval(existCondition);
                      svgPanZoom(svg_el, {pan_zoom_json});
                  }}
                  if (--attempts == 0) {{
                      console.warn("SVG element not found, zoom wont work");
                      clearInterval(existCondition);
                  }}
                }}, 100); // check every 100ms
            </script>
            {svg_txt}
        </div>
    '''
    return HTML(html)
