from manimlib.imports import *


WEIERSTEP = 0.0001

MAX_SERIES_ORDER = 10

SERIES_RUN_TIME = .15
SERIES_STROKE = 2
SERIES_INTERVAL = PI
INTV_LENGTH = 2/(2*SERIES_INTERVAL)
TRIG_MULTIPLIER = 2*PI/(2*SERIES_INTERVAL)

INTEGRAL_PRECISION = 30000
ROUND_PRECISION = int(math.log(INTEGRAL_PRECISION, 10)+1)

ZOOM_ITERATIONS = 5


def integrate(function, interval):
  points = np.linspace(interval[0], interval[1], INTEGRAL_PRECISION)
  fx = [function(point) for point in points]
  area = np.sum(fx)*(interval[1]-interval[0])/INTEGRAL_PRECISION
  return round(area, ROUND_PRECISION)

def calculate_fourier_series(f, N, x):
  series = [integrate(f, (-1, 1))/2]
  for n in range(1,N+1):
    f_a_n = lambda x : f(x)*np.cos(PI*n*x)
    f_b_n = lambda x : f(x)*np.sin(PI*n*x)
    a_n = integrate(f_a_n, (-1, 1))
    b_n = integrate(f_b_n, (-1, 1))
    series.append(a_n*np.cos(PI*n*x)+b_n*np.sin(PI*n*x))
  return sum(series)

def calculate_a_ns(f, N):
  a_ns = []
  for n in range(1,N+1):
    a_ns.append(INTV_LENGTH* integrate(lambda x : (f)(x)*np.cos(TRIG_MULTIPLIER*n*x), (-SERIES_INTERVAL, SERIES_INTERVAL)))
  return a_ns

def calculate_b_ns(f, N):
  b_ns = []
  for n in range(1,N+1):
    b_ns.append(INTV_LENGTH* integrate(lambda x : (f)(x)*np.sin(TRIG_MULTIPLIER*n*x), (-SERIES_INTERVAL, SERIES_INTERVAL)))
  return b_ns





seriesColors = [
  ("#336B87", "#90AFC5"), 
  ("#C0C684", "#F67280"),
  ("#F98866", "#FF420E"),
  ("#6C5B7B", "#F8B195"), 
  ("#80BD9E", "#89DA59"), 
  ("#66A5AD", "#07575B"), 
  ("#A94425", "#A43820"), 
  ("#505160", "#68829E"), 
  ("#375E97", "#FFBB00"), 
  ("#CD6911", "#F4CC70"), 
  ("#1E434C", "#8D230F"),
  ]

# lambda x : (0 if x<=-PI/2 or x>=PI/2 else (x+PI if x<=0 else -x+PI)),

# If graph is discontinuous it needs to be defined thorugh more than one lambda
# is this is the case, the first element of the list is the list of discontinuities
# assert(len(functions[i][0]) = len(functions[i][1:])-1)
functions = [ 
  [[], lambda x : 1 if x==0 or x==1 else x**2 * np.sin(PI/(2*x))+(x-1)*np.sin(PI/(2*(x-1)))],
  [[], lambda x : PI*np.sin((1/1.75*(x+PI))**(1/1.75*(x+PI)))/(1+(1/1.75*(x+PI))**2)],
  [[], lambda x : x],
  [[], lambda x : 0 if x == -PI else (x+PI)*np.cos(1/math.log(1/(x+PI)))],
  [[], lambda x : PI/2*(1/PI*x)**3],
  [[PI*i for i in [-0.75, -0.5, -.25, 0, .25, .5, .75]], lambda x : -PI, lambda x : -PI*3/4, lambda x : -PI*2/4, lambda x : -PI*1/4, lambda x : 0, lambda x : PI*1/4, lambda x : PI*2/4, lambda x : PI*3/4],
  [[], lambda x : 2**(-1/PI*x)],
  [[], lambda x : math.log(x+PI+1/50)],
  [[], lambda x : math.atan(x)],
]

functions2 = [ 
  lambda x : 1 if x==0 or x==1 else x**2 * np.sin(PI/(2*x))+(x-1)*np.sin(PI/(2*(x-1))),
  lambda x : PI*np.sin((1/1.75*(x+PI))**(1/1.75*(x+PI)))/(1+(1/1.75*(x+PI))**2),
  lambda x : x,
  lambda x : 0 if x == -PI else (x+PI)*np.cos(1/math.log(1/(x+PI))),
  lambda x : PI/2*(1/PI*x)**3,
  lambda x : PI*(-1 if x <=-PI*.75 else (-3/4 if x<=-PI*.5 else (-.5 if x<=-PI*.25 else (-.25 if x <=0 else (0 if x<=PI*.25 else (.25 if x<=PI*.5 else (.5 if x<=PI*.75 else .75))))))),
  lambda x : 2**(-1/PI*x),
  lambda x : math.log(x+PI+1/50),
  lambda x : math.atan(x),
]

funcPrecision = [0.0001, 0.0001, 0.0005, 0.0001, 0.0005, 0.0001, 0.0005, 0.0001, 0.0005]
funcOrderRuntimes = [(160, .075), (130, .1), (80, .15), (115, .1), (80, .15), (130, .1), (80, .15), (100, .125), (80, .15)]
funcNameCorners = [UL, DL, UL, DR, UL, UL, DL, UL, UL]
funcNameScaleBuffs = [(.5, .55), (.55, .75), (.65, 1.3), (.6, 1), (.65, 1.3), (.65, 1.3), (.65, 1.4), (.6, .9), (.6, 1.3)]
functionNames = [
  """$f(x) = \\begin{cases}
  x^2 \\sin\\frac{\\pi}{2x} + (x-1)\\sin\\frac{\\pi}{2(x-1)},\\ \\ x\\in \\{0,1\\}\\\\
  1\\ \\ \\text{if } x = 0 \\vee x = 1 \\\\
  \\end{cases}$ \\vspace{.3cm}\\\\
  {\\footnotesize a terrifying function that appeared in my Calc I final}""",
  "$ f(x) = \\dfrac{ \\sin\\left( {\\left( \\frac{1}{x} \\right) }^{\\frac{1}{x}} \\right) }{1+x^2}\\ \\ ${\\small(scaled and shifted)}",
  """$ f(x)=x $\\vspace{.3cm}\\\\
  simple but hypnotizing""",
  """$f(x) = \\begin{cases}
  (x+\\pi)\\cos\\left( \\frac{1}{\\ln\\frac{1}{x+\\pi}} \\right) & \\text{if } x\\neq 0 \\\\
    0 & \\text{if } x = 0
  \\end{cases}$""",
  "$f(x) = x^3\\ \\ ${\\small(scaled)}",
  "$ f(x)=\\lfloor x \\rfloor\\ \\ ${\\small(scaled)}",
  "$ f(x) = 2^{-\\frac{1}{\\pi x}} $",
  "$ f(x) = \\ln(x+\\pi)\\ \\ ${\\small(shifted)}",
  "$ f(x) = \\arctan(x)\\ \\ ${\\small (scaled)}"
]
functionNames = [TextMobject(functionNames[i], alignment="\\flushleft", background_stroke_width=0).scale(funcNameScaleBuffs[i][0]).to_corner(funcNameCorners[i], buff=funcNameScaleBuffs[i][1]) for i in range(len(functions2))]
functionNames = [functionNames[i].set_color_by_gradient(seriesColors[i][0], seriesColors[i][1]) for i in range(len(functionNames))]

class Fourier(GraphScene):
  CONFIG = {
    # "camera_config": {"background_color": WHITE},
    "camera_config": {"background_color": BG_GREY},
    "x_axis_label": "",
    "y_axis_label": "",
    "y_max" : PI,
    "y_min" : -PI,
    "x_max" : SERIES_INTERVAL,
    "x_min" : -SERIES_INTERVAL,
    "y_tick_frequency" : PI/2,
    "x_tick_frequency" : PI/2,
    "axes_color" : WHITE,
    "graph_origin": np.array((0,0,0)),
    "num_graph_anchor_points":75,
  }
  
  def Range(self, in_val,end_val,step=1):
    return list(np.arange(in_val,end_val+step,step))

  def get_functions(self, i):
    dummy = functions[i]
    finalGraphs = []
    # if not dummy[0]:
    for j in range(len(functions[i][1:])):
      finalGraphs.append(
        self.get_graph(
          functions[i][j+1],
          color=seriesColors[i][0], 
          x_min=(-SERIES_INTERVAL if j==0 else functions[i][0][j-1]), 
          x_max=(SERIES_INTERVAL if j==len(functions[i][1:])-1 else functions[i][0][j]),
          step_size=WEIERSTEP, 
          stroke_width=3 ))
    # else:
      # finalGraphs.append(ParametricFunction(lambda t : [(functions[i][1])(t), (functions[i][2])(t), 0], color=GRAPH_COLOR, t_min = functions[i][0][0], t_max = functions[i][0][1]))
    return finalGraphs

  def weierstrass_order_i(self, i, t):
    a = 0.5
    b = 3
    return sum([a**k*np.cos(b**k * np.pi * t) for k in range(0,i+1)])


  def construct(self):
    self.setup_axes()
    for i in range(len(functions)):
      functions_i = self.get_functions(i)
      self.play(
        AnimationGroup(*[ShowCreation(graph, run_time=2/len(functions_i)) for graph in functions_i], lag_ratio=0.85),
        FadeIn(functionNames[i], run_time=1.5)
      )
      self.wait()
      a_0 = INTV_LENGTH*integrate(functions2[i], (-SERIES_INTERVAL, SERIES_INTERVAL))
      print("aaa")
      a_ns = calculate_a_ns(functions2[i], funcOrderRuntimes[i][0])
      print("b")
      b_ns = calculate_b_ns(functions2[i], funcOrderRuntimes[i][0])
      print("c")
      graphs = [
        self.get_graph(
          lambda x : a_0/2+a_ns[0]*np.cos(TRIG_MULTIPLIER*x)+b_ns[0]*np.sin(TRIG_MULTIPLIER*x), 
          color=seriesColors[i][1], 
          x_min = -SERIES_INTERVAL, 
          x_max = SERIES_INTERVAL, 
          stroke_width=SERIES_STROKE, 
          step_size=funcPrecision[i])
      ]
      print("Function "+str(i+1)+" order "+str(1))
      nText = TextMobject("$n=1$").scale(.8).to_corner(UR, buff=.5).set_opacity(.6)
      self.play(
        ShowCreation(graphs[0]),
        Write(nText), run_time=1.5)
      self.wait(.9)
      self.play(ApplyMethod(functionNames[i].set_opacity, .65), run_time=.3)
      for n in range(1, funcOrderRuntimes[i][0]+1):
        # print("Function "+str(i+1)+" order "+str(n+1))
        graphs.append(self.get_graph(
          lambda x : sum([a_0/2, *[a_ns[j]*np.cos(TRIG_MULTIPLIER*(j+1)*x)+b_ns[j]*np.sin(TRIG_MULTIPLIER*(j+1)*x) for j in range(n)]]),
          color = seriesColors[i][1],
          x_min = -SERIES_INTERVAL,
          x_max = SERIES_INTERVAL,
          stroke_width=SERIES_STROKE,
          step_size=funcPrecision[i]))
        self.play(
          Transform(graphs[0], graphs[n]),
          Transform(nText, TextMobject("$n="+str(n+1)+"$").scale(.8).move_to(nText).set_opacity(.6)), run_time=funcOrderRuntimes[i][1])
      self.wait(.5)
      self.play(*[FadeOut(graph) for graph in [nText, functionNames[i]]+functions_i+[graphs[0]]])
    self.wait()

    title = TexMobject("f(x)=\\displaystyle\\sum_{i=0}^","{\\infty}", "a^n \\cos(b^n\\pi x)").set_color_by_gradient(BLUE_B, BLUE_D).set_color(MATI_PASTEL_RED).scale(.7).to_corner(UL, buff=1.05)
    funcNameWeier = TextMobject("Weierstrass function").scale(.7).set_color_by_gradient(BLUE_B, BLUE_D).to_corner(UR, buff=1.31)
    graphs = [
      self.get_graph(
        lambda t: PI/2*self.weierstrass_order_i(0, t/PI), 
        color=BLUE_C, 
        x_min =-SERIES_INTERVAL , 
        x_max = SERIES_INTERVAL, 
        step_size=WEIERSTEP, 
        stroke_width = 1)
      ]
    print("Weierstrass 1")
    self.play(
      ShowCreation(graphs[0]),
      Write(title),
      Write(funcNameWeier),
      run_time = 1.5)
    for i in range(1,10):
      print("Weierstrass "+str(i))
      graphs.append(
        self.get_graph(
          lambda t: PI/2*self.weierstrass_order_i(i, t/PI), 
          color=BLUE_C, 
          x_min = -SERIES_INTERVAL, 
          x_max = SERIES_INTERVAL, 
          step_size=WEIERSTEP, 
          stroke_width = 1))
      self.play(Transform(graphs[0], graphs[i-1], run_time=.8))
      self.wait(.1)
    self.wait(.7)
    self.play(*[FadeOut(x) for x in self.mobjects])

    GraphScene.setup_axes(self)
    self.remove(self.axes, self.x_axis, self.y_axis)
    self.wait(1.2)
    finalGraph = self.get_graph(
      lambda t: PI/2*self.weierstrass_order_i(100, t/PI), 
      color=BLUE_C, 
      x_min =-SERIES_INTERVAL, 
      x_max = SERIES_INTERVAL, 
      step_size=0.00001, 
      stroke_width = 1)
    zoomText = TextMobject(
      """Continuous everywhere\\\\
        Differentiable nowhere""", color=MATI_PASTEL_RED).scale(.6).to_corner(UL, buff=.7)
    frame = RoundedRectangle(corner_radius=.1, color=MATI_PASTEL_RED, width=3.4, height=1.15, stroke_width=1.5).move_to(zoomText)
    self.play(FadeIn(finalGraph), ShowCreation(VGroup(zoomText, frame)), run_time=3)
    self.wait(1.7)
    for i in range(5):
      coordBack = finalGraph.get_edge_center(UP)
      finalGraph.generate_target()
      finalGraph.target.scale(1.9)
      finalGraph.target.shift(coordBack-finalGraph.target.get_edge_center(UP))
      self.play(MoveToTarget(finalGraph), run_time=2.05)
      self.wait(.3)
    self.wait(2)
    self.play(*[FadeOut(x) for x in self.mobjects], run_time=3)
    self.wait(1.6)

  def setup_axes(self):
    GraphScene.setup_axes(self)
    self.axes.set_stroke(width=3)
    self.axes.set_opacity(.5)
    x_label = TextMobject("$x$").scale(.75).set_opacity(.5).next_to(self.x_axis, RIGHT, buff=.17)
    y_label = TextMobject("$y$").scale(.75).set_opacity(.5).next_to(self.y_axis, UP, buff=.17)
    # self.x_axis_label.next_to(self.x_axis, direction=RIGHT)
    # self.y_axis_label.next_to(self.y_axis, direction=UP

    # self.x_axis.add_numbers(*[-PI,-PI/2, PI/2, PI])
    self.y_axis.label_direction = LEFT

    values_decimal_x=self.Range(-PI,PI,PI/2)
    # list_y = [*["%s"%i for i in values_decimal_y]]
    list_x = ["-\\pi", "", "", "", "\\pi"]
    # list_x = ["-\\pi", "-\\frac{\\pi}{2}", "", "\\frac{\\pi}{2}", "\\pi"]
    values_x = [(i,j) for i,j in zip(values_decimal_x,list_x)]
    # if (0.0, '0.0') in values_y:
    #   values_y[values_y.index((0.0, '0.0'))] = (0.0, '')
    # elif (0, '0') in values_y:
    #   values_y[values_y.index((0, '0'))] = (0, '')
    self.x_axis_labels = VGroup()
    for x_val, x_tex in values_x:
      tex = TexMobject(x_tex).set_opacity(.6)
      tex.scale(0.7)
      tex.next_to(self.coords_to_point(x_val, 0), DOWN)
      self.x_axis_labels.add(tex)


    # values_decimal_y=self.Range(-2,2,1)
    values_decimal_y=self.Range(-PI,PI,PI/2)
    # Transform positions to tex labels
    # list_y = [*["%s"%i for i in values_decimal_y]]
    list_y = ["-\\pi", "", "", "", "\\pi"]
    # list_y = ["-\\pi", "-\\frac{\\pi}{2}", "", "\\frac{\\pi}{2}", "\\pi"]
    # List touples of (position,label)
    values_y = [(i,j) for i,j in zip(values_decimal_y,list_y)]
    if (0.0, '0.0') in values_y:
      values_y[values_y.index((0.0, '0.0'))] = (0.0, '')
    elif (0, '0') in values_y:
      values_y[values_y.index((0, '0'))] = (0, '')
    self.y_axis_labels = VGroup()
    for y_val, y_tex in values_y:
      tex = TexMobject(y_tex).set_opacity(.6)
      tex.scale(0.7)
      tex.next_to(self.coords_to_point(0,y_val), LEFT)
      self.y_axis_labels.add(tex)

    self.play(
      Write(self.y_axis),
      Write(self.y_axis_labels),
      Write(self.x_axis),
      Write(self.x_axis_labels),
      Write(x_label),
      Write(x_label),
    )


