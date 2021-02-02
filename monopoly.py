# monopoly.py

from manimlib.imports import *
from manimlib.board import *

def clear_scene(self):
  self.play(*[FadeOut(mob) for mob in self.mobjects])

class ScenePar1(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def build1(self, locations, tiny, texts, tags, colors):
    tiny.set_fill(colors)
    tiny.move_to(locations, aligned_edge=UP)
    texts.scale(.65)
    texts.next_to(tiny, direction=DOWN)
    tags.next_to(locations.get_edge_center(DOWN), direction=UP, buff=.2)
    locations.set_stroke(width=5.5)
    tiny.set_stroke(width=5.5)

  def construct(self):
    title = TextMobject("Monopoly", color=MATI_SALMON).scale(1.5)
    self.play(Write(title), run_time=5.5)
    self.wait(.5)
    self.play(FadeOut(title))
    self.wait(.5)

    # N. of Players
    nPlayers = TextMobject("N$^\\circ $ of players")
    players = [Dot(radius=.2, color=MATI_SALMON) for i in range(4)]
    playersGroup = VGroup(*players)
    playersGroup.arrange(RIGHT, buff=.3)
    group1 = VGroup(nPlayers, playersGroup)
    group1.arrange(DOWN, buff=.7)
    self.play(Write(nPlayers), FadeIn(playersGroup), run_time=.5)
    for i in range(2,5):
      self.play(*[Indicate(players[k], color=MATI_YELLOW, run_time=0.3) for k in range(i)])
    self.play( 
      group1.to_corner, UL,
      group1.scale, 0.6,
      run_time=.5
    )
    

    # Example cards
    w = 2
    h = 3
    locations = [Rectangle(width=w, height=h) for _ in [0,1]]
    tiny = [Rectangle(fill_opacity=1, width = w, height = h/4) for _ in [0,1]]
    texts = [TextMobject("""Baltic\\\\
      Ave.""",), TextMobject("Broadwalk")]
    tags = [TextMobject("\\$"), TextMobject("\\$\\$\\$")]
    colors = [MONOPOLY_BROWN, MONOPOLY_BLUE]
    group2 = VGroup(locations[0], locations[1])
    group2.arrange(RIGHT, buff=.5)
    for i in [0,1]:
      self.build1(locations[i], tiny[i], texts[i], tags[i], colors[i])
    balticBroadwalkGroup = VGroup(group2, tiny[0], tiny[1], texts[0], texts[1], tags[0], tags[1])
    self.play(ShowCreation(group2), FadeIn(tiny[0]), FadeIn(tiny[1]),
      Write(texts[0]), Write(texts[1]), Write(tags[0]), Write(tags[1]), run_time=1)
    self.play(
      balticBroadwalkGroup.to_corner, DR, 
      balticBroadwalkGroup.scale, 0.6,
      run_time=.5)


    # Houses and hotels
    house1 = Rectangle(width=.5, height=.4, fill_opacity=1, color=HOUSE_GREEN).scale(0.8)
    house2 = Polygon(house1.get_corner(UL), house1.get_corner(UR), house1.get_edge_center(UP)+(0, 0.8* .25, 0), fill_opacity=1, color=HOUSE_GREEN)
    house = VGroup(house1, house2).arrange(UP, buff=0)
    hotel1 = Rectangle(width=1, height=.44, fill_opacity=1, color=HOUSE_RED).scale(0.8)
    hotel2 = Polygon(hotel1.get_corner(UL), hotel1.get_corner(UR), hotel1.get_edge_center(UP)+(0, 0.8* .25, 0), fill_opacity=1, color=HOUSE_RED)
    hotel = VGroup(hotel1, hotel2).arrange(UP, buff=0)
    houseTexts = TextMobject("$4$", "$\\times$", "$\\longrightarrow$", "$1$", "$\\times$")
    houseFrame = RoundedRectangle(width = 5.5, height=1.5, corner_radius=0.5).set_stroke(width=1.8)
    houseAndHotel = VGroup(houseTexts[0], houseTexts[1], house, houseTexts[2], houseTexts[3], houseTexts[4], hotel).arrange(RIGHT, buff=0.3)

    self.play(FadeIn(houseAndHotel, UP), ShowCreation(houseFrame), run_time=1)
    self.play(houseAndHotel.scale, 0.6, houseFrame.scale, 0.6)
    # self.play(FadeOut(group1), FadeOut(balticBroadwalkGroup), FadeOut(houseAndHotel), FadeOut(houseFrame))
    self.wait(4)
    clear_scene(self)
    

    # Board stuff
    setup_board(self)
    boardAndTextGroup.scale(.9)
    textLongTerm = TextMobject("Long term probabilities", color=MATI_SALMON).scale(.8)
    boardAndTextGroupAndLongTerm = Group(textLongTerm, boardAndTextGroup).arrange(RIGHT, buff=1)
    # show_board(self, True, 1)
    self.play(FadeIn(boardAndTextGroupAndLongTerm))
    self.play(Indicate(textLongTerm, color=MATI_YELLOW))
    self.wait(.5)
    player, lastSquare = set_player(self, 1, 60, 1, 0, 0.1)

    clear_scene(self)

class ScenePar2(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):

    # Titles
    t1 = TextMobject("Monopoly", color=MATI_SALMON).scale(1.25)
    t2 = TextMobject("Markov Chains", color=MATI_SALMON).scale(1.25)
    self.play(FadeIn(t1))
    self.wait(1)
    self.play(Transform(t1, t2))
    self.wait(1.5)

    # Board stuff
    setup_board(self)
    self.play(FadeOutAndShift(t1), FadeIn(boardGroup))
    player, lastSquare = set_player(self, 1, 6, 2, 0, 1.5, [1, 11, 18, 25, 32, 38, 9])

    # Matrix
    dummyMatrix = """$$P = \\begin{bmatrix}
    P_{1,1} & P_{1,2} & P_{1,3} &  & P_{1,40} \\\\
    P_{2,1} & P_{2,2} & P_{2,3} & \\cdots & P_{2,40}\\\\
    P_{3,1} & P_{3,2} & P_{3,3} &  & P_{3,40}\\\\
     & \\vdots & & \\ddots & \\vdots \\\\
    P_{40,1} & P_{40,2} & P_{40,3} & \\cdots & P_{40,40}
    \\end{bmatrix}$$"""
    dummyMatrixMObject = TextMobject(dummyMatrix)
    dummyMatrix2 = TextMobject("$P_{a,b}=$ probability of going \\textbf{\\textit{from}} square $a$\\\\ \\textbf{\\textit{to}} square $b$ in one turn")
    rowSumsOne = TextMobject("$\\displaystyle\\sum_{i=1}^{40} P_{a,i}=40\\ \\ \\ $", "(rows sum one)")
    dummyMatrixGroup = VGroup(dummyMatrixMObject, dummyMatrix2, rowSumsOne).scale(.65).arrange(DOWN, buff=.6)
    self.play(
      Group(player, boardGroup).shift, 4*RIGHT)
    dummyMatrixGroup.to_edge(LEFT, buff=1)
    self.wait(2)
    self.play(Write(dummyMatrixMObject))
    self.wait(3)
    self.play(Write(dummyMatrix2), run_time=3)
    self.wait(5.5)
    self.play(Write(rowSumsOne[0]), Write(rowSumsOne[1]))
    self.wait(.5)
    self.play(Indicate(rowSumsOne[1], color=MATI_YELLOW))
    self.wait()
    matrixNameArrow = CurvedArrow(start_point=1.6*UP, end_point=1.5*RIGHT+2.8*UP)
    matrixName = TextMobject("Step transition matrix").scale(.75)
    matrixName.next_to(matrixNameArrow.get_end(), direction=UP, buff=.1)
    self.play(ShowCreation(matrixNameArrow))
    self.play(Write(matrixName))
    self.wait(9.5)
    squares140texts = [TextMobject(str(i)) for i in [1,40]]
    squares140texts[0].scale(1.2)
    squares140texts[1].scale(.5)
    squares140texts[0].move_to(bigSquares[2].get_center())
    squares140texts[1].move_to(littleSquares[1][8].get_center()+0.05*RIGHT)
    self.play(Write(squares140texts[0]))
    self.wait(.5)
    self.play(Write(squares140texts[1]))
    self.play(*[Flash(squares140texts[i], ) for i in [0,1]])
    clear_scene(self)
    # self.play(ApplyWave(matrixName))




class ScenePar3(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    self.wait(3)
    t1 = TextMobject("Time-homogenous Markov chain", color=MATI_SALMON).scale(1.2)
    self.play(Write(t1), run_time=2)
    self.wait()
    t1.generate_target()
    t1.target.scale(0.75)
    t1.target.to_corner(UL)
    self.play(MoveToTarget(t1))
    setup_board(self)
    self.play(FadeIn(boardGroup))
    player, lastSquare = set_player(self, 15, 300, 1, 0, .02)
    self.wait(2)
    self.play(FadeOut(player))
    # squares = [1, 9, 19, 30, 1, 8, 16, 21, 26, 36, 5, 9, 13, 17, 25, 32, 36, 2, 11, 22, 33, 40, 3, 12, 21, 30, 32, 37, 8, 13, 23, 31, 34, 4, 10, 14, 23, 35, 1, 6, 15, 22, 32, 38, 7, 17, 24, 26, 29, 35, 1]
    squares = [1, 9, 19, 30, 1, 8, 13, 21, 26, 36, 5, 11, 20, 29, 1]
    player, lastSquare = set_player(self, 1, 14, 1, 0, .2, True, squares)
    pProbs = TextMobject("\\underline{Every probability is given by $P$}").scale(0.76).to_edge(LEFT, buff=1.5)
    boardPlayerGroup = Group(player, boardGroup)
    boardPlayerGroup.generate_target()
    boardPlayerGroup.target.to_edge(RIGHT, buff=1.5)
    self.wait(3.5)
    self.play(MoveToTarget(boardPlayerGroup), Write(pProbs), run_time=2)
    self.wait(4)
    clear_scene(self)
    

class ScenePar4(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    setup_board(self)
    dummyMatrix = """$$P = \\begin{bmatrix}
    P_{1,1} & P_{1,2} & P_{1,3} &  & P_{1,40} \\\\
    P_{2,1} & P_{2,2} & P_{2,3} & \\cdots & P_{2,40}\\\\
    P_{3,1} & P_{3,2} & P_{3,3} &  & P_{3,40}\\\\
     & \\vdots & & \\ddots & \\vdots \\\\
    P_{40,1} & P_{40,2} & P_{40,3} & \\cdots & P_{40,40}
    \\end{bmatrix}$$"""
    dummyMatrixMObject = TextMobject(dummyMatrix)
    dummyMatrix2 = TextMobject("$P_{a,b}=$ probability of going \\textbf{\\textit{from}} square $a$\\\\ \\textbf{\\textit{to}} square $b$ in one turn")
    rowSumsOne = TextMobject("$\\displaystyle\\sum_{i=1}^{40} P_{a,i}=40\\ \\ \\ $(rows sum one)")
    dummyMatrixGroup = VGroup(dummyMatrixMObject, dummyMatrix2, rowSumsOne).scale(.65).arrange(DOWN, buff=.6)
    boardGroup.move_to(boardGroup.get_center()+4*RIGHT)
    # self.play(
      # Group(player, boardGroup).shift, 4*RIGHT)
    dummyMatrixGroup.to_edge(LEFT, buff=1)
    matrixNameArrow = CurvedArrow(start_point=1.6*UP, end_point=1.5*RIGHT+2.8*UP)
    matrixName = TextMobject("Step transition matrix").scale(.75)
    matrixName.next_to(matrixNameArrow.get_end(), direction=UP, buff=.1)
    squares140texts = [TextMobject(str(i)) for i in [1,40]]
    squares140texts[0].scale(1.2)
    squares140texts[1].scale(.5)
    squares140texts[0].move_to(bigSquares[2].get_center())
    squares140texts[1].move_to(littleSquares[1][8].get_center()+0.05*RIGHT)
    self.play(FadeIn(boardGroup), FadeIn(dummyMatrixMObject), FadeIn(dummyMatrix2), FadeIn(rowSumsOne), FadeIn(matrixNameArrow), FadeIn(matrixName), FadeIn(squares140texts[0]), FadeIn(squares140texts[1]))
    self.wait(5)
    clear_scene(self)

    dicePairs = [DicePair(faces=(i+1,j+1)) for j in range(6) for i in range(6)]
    diceGroup = VGroup(*[dicePairs[i] for i in range(36)]).arrange_in_grid(6, 6, buff=0.4)
    self.play(*[ShowCreation(dicePairs[i]) for i in range(36)], run_time=2)
    diceGroup.generate_target()
    diceGroup.target.scale(.7)
    diceGroup.target.to_edge(LEFT)
    self.play(MoveToTarget(diceGroup))
    diceGroupCopy = diceGroup.copy()
    diceGroupTexts = []
    matches = []
    matchesCopy = []
    numbers = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
    nColors = [DICE_2, DICE_3, DICE_4, DICE_5, DICE_6, DICE_7, DICE_6, DICE_5, DICE_4, DICE_3, DICE_2]
    for i in range(2,13):
      matches.append(list(filter(lambda dicePair: True if sum(dicePair.faces) == i else False, diceGroup)))
      matchesCopy.append(list(filter(lambda dicePair: True if sum(dicePair.faces) == i else False, diceGroupCopy)))
      diceGroupTexts.append(TextMobject("Rolls whose sum is " + numbers[i-2] + ": " + str(len(matchesCopy[i-2])) + "/36", color=nColors[i-2]))
    VGroup(*diceGroupTexts).arrange(DOWN).scale(.72).to_edge(RIGHT, buff=1)
    for i in range(11):
      self.play(Transform(VGroup(*matchesCopy[i]), diceGroupTexts[i], run_time=1.5), 
      *[ApplyMethod(matches[i][j].set_color, nColors[i], run_time=1) for j in range(len(matches[i]))])
    self.wait(1.8)
    clear_scene(self)


class ScenePar5(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    matrix = "$$P=\\begin{bmatrix}\n"
    for i in range(40):
      for j in range(40):
        matrix += stepTransitionMatrixOnlyDices[i][j]+(" & " if j!=39 else (" \\\\" if i!=39 else "\n"))
    matrix += "\\end{bmatrix}$$"
    matrixText = TextMobject(matrix, color=MATI_YELLOW, background_stroke_width=0).scale(.22)
    circle = Circle(radius=.1, fill_opacity=0, color=MATI_SALMON).to_corner(UL, buff=1).set_stroke(width=1)
    circle.move_to(circle.get_center()+0.27*LEFT+.325*DOWN)
    arrow = CurvedArrow(start_point=circle.get_edge_center(UP)+.05*RIGHT+.02*DOWN, end_point=circle.get_edge_center(UP)+4*RIGHT, color=MATI_SALMON, angle=-TAU/8, tip_length=.1).set_stroke(width=1)
    self.wait(4)
    self.play(Write(matrixText))
    self.play(ShowCreation(circle))
    self.wait(.7)
    self.play(ShowCreation(arrow), run_time=2)
    self.wait(10)
    clear_scene(self)

class ScenePar6(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    quirksTitle = TextMobject("Monopoly's Probabilistic Quirks", color=MATI_SALMON)
    self.play(Write(quirksTitle))
    self.play(FocusOn(quirksTitle), run_time=3)
    self.wait(5)
    thingsToConsider = TextMobject("Things to consider:\\\\", 'The "Go To Jail" square\\\\', "Chance and Community Chest cards\\\\", "Doubles\\\\")
    thingsToConsider[0].scale(1.3).set_color(MATI_YELLOW)
    for i in range(1,4):
      thingsToConsider[i].scale(.75)
    VGroup(*thingsToConsider).arrange(DOWN)
    self.play(ReplacementTransform(quirksTitle, thingsToConsider[0]), run_time=1.5)
    self.wait(.4)
    self.play(Write(thingsToConsider[1]))
    self.wait(3.7)
    self.play(Write(thingsToConsider[2]))
    self.wait(4.5)
    self.play(Write(thingsToConsider[3]))
    self.wait(4)
    self.play(thingsToConsider[1].to_corner, UL, *[FadeOut(thingsToConsider[i]) for i in [0, 2, 3]])
    self.wait(2)
    setup_board(self)
    boardGroup.to_edge(RIGHT)
    matrix = "Row 31 of $P=\\big(\\  0 \\ \\  0 \\ \\  \\cdots \\  \\overbrace{1}^{P_{31,11}} \\  \\cdots \\ \\  0 \\ \\  0 \\ \\big)$"
    matrix = TextMobject(matrix, background_stroke_width=0).scale(.8).to_edge(LEFT, buff=1.5)
    self.play(FadeIn(boardGroup))
    self.wait()
    player, lastSquare = set_player(self, 24, 2, 2, 0, 1.5, False, [24, 31, 11])
    self.wait(6)
    self.play(Write(matrix))
    self.wait(2)
    self.play(*[FadeOut(x) for x in [player, boardGroup, matrix]])
    
    # thingsToConsider = TextMobject("Things to consider:\\\\", 'The "Go To Jail" square\\\\', "Chance and Community Chest cards\\\\", "Doubles\\\\")
    thingsToConsider[2].to_corner(UL)
    self.play(Transform(thingsToConsider[1], thingsToConsider[2]))

    # CHPlaces = TextMobject("Sent from Community Chest", "Jail", "Go")
    # ChancePlaces = TextMobject("Sent from \\overbrace{Community Chest}", "^\\{\\times 16\\}", "Reading Railroad", "Illinois Ave.", "St. Charles Place", "Broadwalk", "Jail", "Go", "Nearest Railroad ($\\times 2$)", "Nearest Utility", "\\textit{[Go back three spaces]}")
    # CHPLaces[0].set_color(MATI_YELLOW)
    # ChancePLaces[0].set_color(MATI_YELLOW)
    # CHGroup = VGroup(*CHPlaces).scale(.7).arrange(DOWN)
    # CGroup = VGroup(*ChancePlaces).scale(.7).arrange(DOWN)
    # CCHGroup = VGroup(CGroup, CHGroup).arrange(RIGHT, buff=.7)
    # self.play(FadeIn(CCHGroup), run_time=1.2)


    # thingsToConsider = TextMobject("Things to consider:\\\\", 'The "Go To Jail" square\\\\', "Chance and Community Chest cards\\\\", "Doubles\\\\")
    # thingsToConsider[0].scale(1.3).set_color(MATI_YELLOW)
    # for i in range(1,4):
      # thingsToConsider[i].scale(.75)
      # thingsToConsider[i].to_corner(UL)

    # self.play(Transform(thingsToConsider[1], thingsToConsider[2]))
    self.wait()

    CHPlacesTitle = TextMobject("Sent from $\\overbrace{\\text{Community Chest}}^{\\text{16 cards}}$\\\\", color=MATI_YELLOW, background_stroke_width=0)
    CHPlaces = TextMobject("Jail\\\\", "Go\\\\")
    ChancePlacesTitle = TextMobject("Sent from $\\overbrace{\\text{Chance}}^{\\text{16 cards}}$\\\\", color=MATI_YELLOW, background_stroke_width=0)
    ChancePlaces = TextMobject("Reading Railroad\\\\", "Illinois Ave.\\\\", "St. Charles Place\\\\", "Broadwalk\\\\", "Jail\\\\", "Go\\\\", "\\textit{(Go back three spaces)}\\\\", "Nearest Railroad ($\\times 2$)\\\\", "Nearest Utility\\\\", background_stroke_width=0)
    CHGroup = VGroup(CHPlacesTitle, VGroup(*CHPlaces).arrange(DOWN, buff=.25)).scale(.65).arrange(DOWN, buff=.4)
    CGroup = VGroup(ChancePlacesTitle, VGroup(*ChancePlaces).arrange(DOWN, buff=.25)).scale(.65).arrange(DOWN, buff=.4)
    CCHGroup = VGroup(CGroup, CHGroup).arrange(RIGHT, buff=.7)
    CHGroup.move_to(CHGroup.get_center()+1.505*UP)
    self.play(FadeIn(CCHGroup), run_time=1.2)
    self.wait(13.5)
    self.play(CGroup.to_edge, LEFT, FadeOut(CHGroup))

    pText = TextMobject("$p=P_{x,\\text{ChanceSquare}}$", "$x=$ some square", color=MATI_RED)
    pTextGroup = VGroup(*pText).arrange(UP).scale(.7).to_edge(RIGHT, buff=1.1)#.shift(2*UP)
    pTextFrame = RoundedRectangle(width=3.5, height=1.5 , corner_radius=.3).move_to(pTextGroup.get_center()).set_stroke(width=1.5)
    self.play(Write(VGroup(pTextGroup, pTextFrame)), run_time=2.5)
    self.wait(5.5)

    pPlacesChance = ["Reading", "Illinois", "Charles", "Broadwalk", "Jail", "Go", "Chance-3", "NearestRd", "NearestUt"]
    pPlacesChance2 = TextMobject(*["$\\longrightarrow P_{x\\text{,"+i+"}}:=P_{x\\text{,"+i+"}}$\\\\" for i in pPlacesChance], background_stroke_width=0)
    pPlacesChance3 = TextMobject(*["$+\\frac{"+("1" if i!="NearestRd" else "2")+"}{16}p$\\\\" for i in pPlacesChance], color=MATI_YELLOW)
    pPlacesChance3[7].set_color(MATI_SALMON)
    for i in range(len(pPlacesChance)):
      pPlacesChance2[i].scale(.65)
      pPlacesChance3[i].scale(.65)
      pPlacesChance2[i].next_to(ChancePlaces[i], direction=RIGHT)
      pPlacesChance3[i].next_to(pPlacesChance2[i], direction=RIGHT, buff=0.075)
      self.play(Write(pPlacesChance2[i]),run_time=.6)
      self.play(Write(pPlacesChance3[i]), run_time=.3)
    pText2 = TextMobject("$p:=\\frac{3}{8}p$", color=MATI_RED).scale(.7).move_to(pText[0])
    self.play(Transform(pText[0], pText2), run_time=1.5)

    self.wait(3)
    CHGroup.to_edge(LEFT)
    pText3 = TextMobject("$p=P_{x,\\text{CommChestSquare}}$", color=MATI_RED).scale(.7).move_to(pText2)
    self.play(
      Transform(CGroup, CHGroup, run_time=2.5), 
      Transform(pText[0], pText3, run_time=2.5), 
      *[FadeOut(x) for x in pPlacesChance2], 
      *[FadeOut(x) for x in pPlacesChance3],
      ApplyMethod(pTextFrame.set_width, pTextFrame.get_width()+.5, run_time=2.5),
    )
    pPlacesCC = ["Jail", "Go"]
    pPlacesCC2 = TextMobject(*["$\\longrightarrow P_{x\\text{,"+i+"}}:=P_{x\\text{,"+i+"}}$\\\\" for i in pPlacesCC], background_stroke_width=0)
    pPlacesCC3 = TextMobject(*["$+\\frac{1}{16}p$\\\\" for i in pPlacesCC], color=MATI_YELLOW)
    self.wait(4)
    for i in range(len(pPlacesCC)):
      pPlacesCC2[i].scale(.65)
      pPlacesCC3[i].scale(.65)
      pPlacesCC2[i].next_to(CHPlaces[i], direction=RIGHT)
      pPlacesCC3[i].next_to(pPlacesCC2[i], direction=RIGHT, buff=0.075)
      self.play(Write(pPlacesCC2[i]),run_time=.6)
      self.play(Write(pPlacesCC3[i]), run_time=.3)
    self.wait()
    self.play(Transform(pText[0], TextMobject("$p:=\\frac{7}{8}p$", color=MATI_RED).scale(.7).move_to(pText3)), run_time=1.5)
    self.wait(12)

    clear_scene(self)


class ScenePar7(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    thingsToConsider = TextMobject("Things to consider:\\\\", 'The "Go To Jail" square\\\\', "Chance and Community Chest cards\\\\", "Doubles\\\\")
    thingsToConsider[0].scale(1.3).set_color(MATI_YELLOW)
    for i in range(1,4):
      thingsToConsider[i].scale(.75)
    thingsToConsider[3].move_to(ORIGIN)
    self.play(Write(thingsToConsider[3]), run_time=2)
    self.wait(17)
    dicePairs = [DicePair(faces=(i+1,j+1)) for j in range(6) for i in range(6)]
    diceGroup = VGroup(*[dicePairs[i] for i in range(36)]).arrange_in_grid(6, 6, buff=0.4)
    doubles = list(filter(lambda dicePair: True if dicePair.faces[0] == dicePair.faces[1] else False, diceGroup))
    doublesGroup = VGroup(*doubles)
    self.play(
      ApplyMethod(thingsToConsider[3].to_corner, UL),
      ShowCreation(diceGroup),
    )
    self.play(
      FadeToColor(doublesGroup, color=MATI_RED),
    )
    
    animations = []
    for i in range(1,len(doubles)):
      animations.append(Swap(doubles[i], diceGroup[i]))
    self.play(AnimationGroup(*animations))
    brace = Brace(doublesGroup, direction=RIGHT)
    oneSixth = TextMobject("$\\frac{1}{6}$").next_to(brace)
    braceGroup = VGroup(brace, oneSixth)
    self.wait(2.5)
    self.play(FadeIn(braceGroup))
    dices = [VGroup(doublesGroup, braceGroup).copy()]
    dices[0].move_to(ORIGIN)
    dices = dices + [dices[0].copy() for _ in [0,1]]
    VGroup(*dices).arrange(DOWN).scale(.65).to_edge(LEFT)
    self.wait(3)
    self.play(
      FadeOut(VGroup(diceGroup, braceGroup)),
      *[FadeIn(dices[i]) for i in range(3)],)
    brace2 = Brace(VGroup(*dices), direction=RIGHT)
    oneSixth3 = TextMobject("$\\frac{1}{6^3}$").next_to(brace2)
    self.play(ShowCreation(VGroup(brace2, oneSixth3)))
    oneThird = TextMobject("$\\cdot \\frac{1}{3}$").next_to(oneSixth3, buff=.11)
    self.wait(4)
    self.play(Write(oneThird))
    self.wait()
    self.play(*[FadeOut(x) for x in [brace2, oneSixth3, oneThird, *dices]])
    epsilon = TextMobject("$\\varepsilon =\\frac{1}{6^3 3}$").next_to(oneSixth3, buff=.11)
    epsilon.move_to(ORIGIN)
    self.wait()
    self.play(Write(epsilon))
    self.play(Flash(epsilon, color=MATI_YELLOW, flash_radius= 1, line_length=0.55))
    stxt = ['"this row of $P$": some arbitrary row',
      "$\\displaystyle\\sum_{i=1}^{40} p_i = 1 $", 
      "$\\displaystyle\\sum_{i=1}^{40} p_i + \\varepsilon$", 
      "$\\alpha \\left( \\displaystyle\\sum_{i=1}^{40} p_i + \\varepsilon \\right)$",
      "$\\alpha \\left( \\displaystyle\\sum_{i=1}^{40} p_i + \\varepsilon \\right) =1$",
      "$\\displaystyle\\sum_{i=1}^{40} p_i=1 \\Longrightarrow$",
      "$\\alpha \\left( \\displaystyle\\sum_{i=1}^{40} p_i + \\varepsilon \\right) = \\alpha ( 1+\\varepsilon )$",
      "$\\alpha ( 1+\\varepsilon ) =1\\ \\iff\\ \\alpha = \\dfrac{1}{1+\\varepsilon}$"]
    stxt = [TextMobject(x, background_stroke_width=0).scale(.7) for x in stxt]
    stxt[0].scale(.6).to_corner(UR)
    self.wait(10)
    self.add(stxt[0])
    self.wait(3)
    self.play(
      FadeIn(stxt[1]),
      FadeOut(stxt[0]),
      ApplyMethod(epsilon.to_corner, UR))
    self.wait(3)
    self.play(Transform(stxt[1], stxt[2]))
    self.wait(2)
    self.play(Transform(stxt[1], stxt[3]))
    self.wait()
    self.play(Transform(stxt[1], stxt[4]))
    self.wait(3)
    stxt[5].shift(2*LEFT)
    dummy = stxt[5].copy()
    self.play(Transform(stxt[1], stxt[5]))
    stxt[6].next_to(stxt[1])
    self.wait()
    self.play(Transform(dummy, stxt[6]))
    self.wait(3)
    stxt[7].shift(.2*DOWN)
    self.play(
      VGroup(dummy, stxt[1]).shift, UP,
      FadeIn(stxt[7])
    )
    self.wait(3)

    result =  "Row $i$ of $P:= \\dfrac{1}{1+\\varepsilon}\\big(\\  P_{i,1} \\ \\  P_{i,2} \\ \\  \\cdots \\  \\overbrace{P_{i,11}+\\varepsilon}^{P_{i,11}} \\  \\cdots \\ \\big)$"
    result = TextMobject(result, background_stroke_width=0, color=MATI_YELLOW).scale(.8)

    self.play(Transform(VGroup(stxt[1], dummy, stxt[7], epsilon, thingsToConsider[3]), result), run_time=2.5)
    self.wait(2)
    clear_scene(self)

    matrix = "$$P\\approx\\begin{bmatrix}\n"
    for i in range(40):
      for j in range(40):
        matrix += str(round(stepTransitionMatrix[i][j], 3))+(" & " if j!=39 else (" \\\\" if i!=39 else "\n"))
    matrix += "\\end{bmatrix}$$"
    matrixText = TextMobject(matrix, color=MATI_YELLOW, background_stroke_width=0).scale(.2)
    self.play(Write(matrixText))
    self.wait(4)
    clear_scene(self)




class ScenePar8(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    setup_board(self)
    initialize_coordinates(self)
    boardAndTextGroup.shift(2.3*RIGHT)
    self.play(FadeIn(boardGroup), FadeIn(TextMobject("No. of times in each square").scale(.85).next_to(boardGroup, direction=LEFT, buff=1)), run_time=.2)
    player, lastSquare = set_player(self, 1, 200, 3, 0, .02)

class ScenePar9(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    limitingDistribution = TextMobject("Limiting Distribution", color=MATI_SALMON)
    self.play(Write(limitingDistribution))
    self.wait(2)
    stxt = ["$\\displaystyle\\lim_{n\\to\\infty}P^n$",
      "If it exists, all rows of $\\displaystyle\\lim_{n\\to\\infty}P^n$ are equal",
      "$=?$",
      "$\\displaystyle\\lim_{n\\to\\infty}\\beta P^n$",
      "Stationary Distribution", 
      """$\\big(\\displaystyle\\lim_{n\\to\\infty}P^n\\big)_{i,j} = \\lambda_j$. Equivalently, the limit dist. is $\\lambda$ such that $\\big(\\ \\lambda_1 \\ \\ \\lambda_2 \\ \\ \\cdots\\ \\ \\lambda_{40}\\ \\big) = \\lambda = \\displaystyle\\lim_{n\\to\\infty}\\beta P^n$ ($\\beta=$ any initial distribution)""",]
      # =\\begin{bmatrix}
      # \\pi_1 & \\pi_2 & \\cdots & \\pi_{40} \\\\
      # \\vdots & \\vdots & \\ddots & \\vdots \\\\
      # \\pi_1 & \\pi_2 & \\cdots & \\pi_{40}
      # \\end{bmatrix}
      # ,\\ \\ \\ \\ \\  \\pi = \\big(\\ \\pi_1 \\ \\ \\pi_2 \\ \\ \\cdots\\ \\ \\pi_{40}\\ \\big)
    stxt = [TextMobject(x).scale(.9) for x in stxt]
    self.play(limitingDistribution.to_corner, UL, FadeIn(stxt[0]), run_time=2)
    self.play(Flash(stxt[0], color=MATI_YELLOW, flash_radius= 1.5, line_length=0.55))
    self.wait(3)
    stxt[5].scale(.6).to_corner(DR)
    self.play(Transform(stxt[0], stxt[1]), Write(stxt[5]), run_time=2)
    self.wait(4)
    stxt[2].set_color(MATI_LIGHT_BLUE).scale(1.2)
    stxt[2].rotate(PI/4)
    stxt[2].next_to(stxt[1], direction=UP).shift(2.29*RIGHT+.17*DOWN)
    self.play(Write(stxt[2]), run_time=3)
    self.wait(3)
    par = ParametricFunction(lambda t: [t, 0.3*np.sin(t), 0], t_min=0, t_max=6*PI, color=MATI_LIGHT_BLUE).scale(.2).move_to(LEFT)
    stxt[3].next_to(par, direction=LEFT)
    stxt[4].scale(.8).next_to(par, direction=RIGHT)
    self.play(Transform(stxt[0],stxt[3],run_time=1.5), FadeOut(stxt[2], run_time=.4), FadeOut(limitingDistribution, run_time=1.5), FadeOut(stxt[5], run_time=.8))
    self.wait()
    self.play(ShowCreation(par), run_time=2)
    self.play(Write(stxt[4]))
    self.play(FocusOn(stxt[4]))
    clear_scene(self)
    stxt.append(TextMobject(
      """If """,
      """$\\beta$""",
      """ is the initial distribution of the chain, then
         the probability of arriving at any state in one step is given by """,
      """$$\\beta P.$$""",
      """Now, if """,
      """$\\pi$""",
      """ is the chain's \\textbf{stationary distribution}
         and we set it as the initial distribution, then the probability of arriving
         at any state after one step will be given \\textit{solely} by $P$. That is, """,
      """$$\\pi P=P$$""", alignment="\\justify", buff=1).scale(.7))
    stxt[6][1].set_color(MATI_YELLOW)
    stxt[6][3].set_color(MATI_YELLOW)
    stxt[6][5].set_color(MATI_LIGHT_BLUE)
    stxt[6][7].set_color(MATI_LIGHT_BLUE)

    self.play(Write(stxt[6][0:4]), run_time=3)
    self.wait()
    self.play(Write(stxt[6][4:]), run_time=5)
    self.wait(2.5)
    self.play(Indicate(stxt[6][7], color=MATI_LIGHT_BLUE, scale_factor=2), run_time=2)
    self.wait(5.5)
    stxt.append(TextMobject("$\\pi$ is \\underline{unique}!").to_corner(DR, buff=.8))
    arrow = CurvedArrow(start_point=stxt[6].get_edge_center(DOWN)+.2*DOWN+.5*LEFT, end_point=stxt[7].get_edge_center(LEFT)+.2*LEFT)
    self.play(ShowCreation(arrow), run_time=1.5)
    self.play(Write(stxt[7]))
    self.wait(1.5)

    stxt.append(TextMobject("uhm... what?").set_color_by_gradient(MATI_SALMON, MATI_RED).to_edge(UP, buff=1))
    self.play(AddTextWordByWord(stxt[8], time_per_char=.5), run_time=5)
    self.wait(11)
    clear_scene(self)



class ScenePar10(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    self.wait()
    setup_board(self)
    initialize_coordinates(self)
    boardGroup.to_edge(RIGHT, buff=1)
    title = TextMobject("Ergodic Markov chains", color=MATI_SALMON).to_edge(UP, buff=.5)
    self.play(FadeIn(boardGroup), Write(title))
    stxt = [TextMobject("The number of times each square is visited\\\\ will eventually be greater than zero").scale(.7).next_to(boardGroup, direction=LEFT, buff=1)]
    self.wait(3.5)
    self.play(Write(stxt[0]), run_time=2)
    player, lastSquare = set_player(self, 1, 200, 3, 0, .02)
    self.wait(3)
    stxt.append(TextMobject("Fundamental Limit Theorem\\\\ for Ergodic Markov Chains").scale(.7).move_to(stxt[0].get_center()+.4*UP))#+2*UP))
    stxt.append(TextMobject("...wonder what it could be about", color=MATI_YELLOW).scale(.36).move_to(stxt[1].get_corner(UL)+.3*UP))
    self.play(FadeOut(stxt[0]), FadeIn(stxt[1]))
    self.wait(2)
    self.play(FadeIn(stxt[2]), run_time=.3)
    self.wait()
    self.play(FadeOut(stxt[2]), run_time=.3)
    stxt.append(TextMobject("$\\displaystyle\\lim_{n\\to\\infty}\\beta P^n$","$=\\pi$").next_to(stxt[1], direction=DOWN, buff=.6).scale(.7))
    self.wait(.25)
    self.play(Write(stxt[3][0]), run_time=1)
    self.wait(2.8)
    self.play(Write(stxt[3][1]), run_time=1.5)
    # self.play(ShowCreation(Circle(color=MATI_YELLOW).move_to(stxt[3]).scale(1.25)),run_time=1)
    self.play(Flash(VGroup(stxt[1], stxt[3]), color=MATI_RED, flash_radius= 3.2, line_length=0.65))
    self.wait(3)
    self.play(VGroup(stxt[1], stxt[3]).shift, 1.4*UP)
    stxt.append(TextMobject("""$\\begin{cases}
      \\pi P = P\\\\
      \\displaystyle\\sum_{i=1}^{40}\\pi_i =1
      \\end{cases}$""").scale(.7).next_to(stxt[3], direction=DOWN, buff=.6))
    self.play(Write(stxt[4]), run_time=2.5)
    self.wait(3)
    clear_scene(self)
    

class ScenePar11(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    a = steadyStates.copy()
    a = [str(round(float(x), 4)) for x in a]
    s = ["$\\pi$","$\\ = \\big("+"\\ \\ ".join(a[:10])+"$\\\\","$"+"\\ \\ ".join(a[10:20])+"$\\\\", "$"+"\\ \\ ".join(a[20:30])+"$\\\\", "$"+"\\ \\ ".join(a[30:])+"\\big)$"]
    s = TextMobject(*s, alignment="\\justify").scale(.6)
    s[0].set_color(MATI_LIGHT_BLUE)
    self.play(Write(s))
    self.play(s.shift, 1.5*UP)

    b = steadyStatesRank.copy()
    b = [str(x) for x in b]
    s2 = ["$\\big($", b[0], *["\\ \\ "+x for x in b[1:]], "$\\big)$"]
    for i in range(1,4):
      s2[10*i] = s2[10*i]+"\\\\"
    s2 = TextMobject(*s2, alignment="\\justify", background_stroke_width=0).scale(.7)

    definitiveRank = [str(x) for x in list(range(1,41))]
    definitiveRank = TextMobject(*definitiveRank).scale(.5)
    colors = [MONOPOLY_RANK_1,MONOPOLY_RANK_2,MONOPOLY_RANK_3,MONOPOLY_RANK_4,MONOPOLY_RANK_5,MONOPOLY_RANK_6,MONOPOLY_RANK_7,MONOPOLY_RANK_8]
    squares = [0, 5, 10, 15, 20, 25, 30, 35]
    for i in range(8):
      for j in range(squares[i]+1, squares[i]+6):
        s2[j].set_color(colors[i])
        definitiveRank[j-1].set_color(colors[i])
    # s2 = ["$\\big("+"\\ \\ ".join(b[:10])+"$\\\\","$"+"\\ \\ ".join(b[10:20])+"$\\\\", "$"+"\\ \\ ".join(b[20:30])+"$\\\\", "$"+"\\ \\ ".join(b[30:])+"\\big)$"]
    finalRank = TextMobject("Final rank: ").scale(.7)
    VGroup(finalRank, s2).arrange(RIGHT)
    VGroup(finalRank, s2).shift(DOWN)
    arrow = Arrow(start=s.get_edge_center(DOWN)+.05*DOWN, end=VGroup(finalRank, s2).get_edge_center(UP)+.05*UP)
    self.play(ShowCreation(arrow, run_time=1.5))
    self.play(Write(finalRank))
    self.play(Write(s2))
    s2.generate_target()
    s2.target.scale(.9)
    s2.target.move_to(ORIGIN)
    s2.target.to_edge(LEFT)
    self.wait(2)
    self.play(FadeOut(VGroup(s, finalRank, arrow)), MoveToTarget(s2),)
    setup_board(self)
    boardAndTextGroup.to_edge(RIGHT)
    coordinatesOfSquares = initialize_coordinates(self)
    show_board(self, True, 1)
    
    animations = []
    for i in range(40):
      definitiveRank[i].move_to(coordinatesOfSquares[int(steadyStatesRank[i])-1])
      animations.append(Transform(s2[i+1], definitiveRank[i]))
    self.play(FadeOut(Group(s2[0],s2[41]), run_time=0.2), AnimationGroup(*animations, lag_ratio=.3))
    self.wait()
    podium = TextMobject("$1^\\circ$", ": Jail\\\\", "$2^\\circ$", ": Illinois Ave.\\\\", "$3^\\circ$", ": Go", alignment="\\flushleft").scale(.7).to_edge(LEFT, buff=1.5)
    colors = [MATI_GOLD, MATI_SILVER, MATI_BRONZE]
    for i in range(3):
      podium[2*i].set_color(colors[i])
    self.play(FadeIn(podium), run_time=2)
    self.wait(22)
    animations = [Indicate(definitiveRank[i-1], color=definitiveRank[i-1].get_color(), scale_factor=1.4) for i in [12, 4, 7]]
    self.play(AnimationGroup(*animations, lag_ratio=.3))
    self.wait(2)
    animations = [Indicate(definitiveRank[i-1], color=definitiveRank[i-1].get_color(), scale_factor=1.4) for i in [2, 5]]
    self.play(AnimationGroup(*animations, lag_ratio=.3))
    self.wait(6)
    arrows = [Arrow(start=bigSquares[0].get_edge_center(LEFT)+2*LEFT, end=bigSquares[0].get_edge_center(LEFT)+.2*LEFT), Arrow(start=bigSquares[0].get_edge_center(UP)+2*UP, end=bigSquares[0].get_edge_center(UP)+.2*UP), Arrow(start=bigSquares[0].get_corner(UL)+UL, end=bigSquares[0].get_corner(UL)+.2*UL)]
    self.play(*[ShowCreation(a) for a in arrows], run_time=2)
    self.wait(1.7)
    self.play(FadeOut(VGroup(*arrows)))
    for i in [1, 3, 4, 36, 38, 39]:
      textNames[i].generate_target()
      textNames[i].target.set_color(properties[i])
    cross = [Cross(textNames[17], stroke_color=RED), Cross(textNames[19], stroke_color=RED)]
    self.play(*[MoveToTarget(textNames[i]) for i in [1, 3, 4, 36, 38, 39]])
    self.play(*[WiggleOutThenIn(textNames[i]) for i in [1, 3, 4, 36, 38, 39]])
    self.wait(4)
    self.play(*[ShowCreation(x) for x in cross], run_time=2)
    self.wait(10)
    self.play(*[Flash(definitiveRank[i-1], color=MATI_YELLOW, flash_radius=0.5) for i in [5,6,8,26]])
    self.wait(12)
    millenium = TextMobject("Millenium Problem solved?", " Nah.").scale(.6).move_to(podium)
    millenium.set_color_by_gradient(DICE_2, DICE_7)
    self.play(
      FadeOut(podium),
      Write(millenium[0], run_time=5)
    )
    self.wait()
    self.play(Write(millenium[1], run_time=2))
    self.wait(2)
    thingsWeDidntConsider = TextMobject("Things we \\textit{didn't} consider:\\\\", "Cost-to-profit ratio of each property\\\\", "Variation in number of players\\\\", "Probably many more...")
    thingsWeDidntConsider[0].scale(.7).set_color_by_gradient(DICE_2, DICE_7)
    for i in range(1,4):
      thingsWeDidntConsider[i].scale(.55)
    VGroup(*thingsWeDidntConsider).arrange(DOWN).move_to(millenium.get_center()+.1*RIGHT)
    self.play(Transform(millenium, thingsWeDidntConsider[0]))
    self.play(Write(thingsWeDidntConsider[1]))
    self.play(Write(thingsWeDidntConsider[2]))
    self.play(Write(thingsWeDidntConsider[3]))
    self.wait(5.5)
    clear_scene(self)



class FinalScene(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    self.wait(1.3)
    txt = [
      TextMobject("Cheers to... math!").set_color_by_gradient(WHITE, MATI_YELLOW),
      TextMobject("Markov chains").scale(1.2).set_color_by_gradient(MATI_SALMON, MATI_RED),
      TextMobject("Monopoly").scale(.8).shift(2.3*UP+3*LEFT),
      TextMobject("Search engines").scale(.8).shift(2.3*UP+3*RIGHT),
      TextMobject("Games of chance").scale(.8).shift(2.3*DOWN+3*LEFT),
      TextMobject("Algorithmic music composition").scale(.8).shift(2.3*DOWN+3*RIGHT),]
    self.play(Write(txt[0]), run_time = 2.5)
    self.wait(2.5)
    self.play(FadeOut(txt[0]))
    rot = [DOWN, DOWN, UP, UP]
    rot2 = [UL, UR, DL, DR]
    arrows = [Line(start=txt[2+i].get_edge_center(rot[i])+.2*rot[i], end=txt[0].get_corner(rot2[i])-.2*rot[i], stroke_width=2.2) for i in range(4)]
    for i in range(2,6):
      self.play(Write(txt[i]))
      self.wait()
    self.play(*[ShowCreation(arrows[i], run_time=2) for i in range(4)], Write(txt[1]))
    self.wait(1.3)
    heart = ParametricFunction(lambda t: [16*((np.sin(t))**3), 13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t), 0], t_min=0, t_max=2*PI, color=MATI_RED, stroke_width=2).scale(.01).rotate(-PI/12).next_to(txt[1], direction=RIGHT).shift(0.1*UP)
    self.play(ShowCreation(heart), run_time=1.5)
    self.play(Flash(heart, flash_radius=.5, color=MATI_RED))

    setup_board(self)
    initialize_coordinates(self)
    self.play(*[FadeOut(mob) for mob in self.mobjects], FadeIn(boardGroup))
    player, lastSquare = set_player(self, 1, 16, 2, 0, .5, False, [1, 8, 14, 20, 27, 36, 6, 17, 25, 31, 11, 21, 30, 33, 4, 13, 17])
    self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)



class FirstScene(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    thingsWeDidntConsider = TextMobject("Things to check out:\\\\", "This\\\\", "That")
    thingsWeDidntConsider[0].scale(1.1).set_color(MATI_YELLOW)
    for i in [1,2]:
      thingsWeDidntConsider[i].scale(.8)
    self.play(Write(thingsWeDidntConsider[0]), run_time=1.4)
    self.play(Write(thingsWeDidntConsider[1]))
    self.play(Write(thingsWeDidntConsider[2]))
    self.wait(.5)
    clear_scene(self)

class Thumbnail(Scene):
  CONFIG = {
    "camera_config": {"background_color": BG_GREY}
  }
  def construct(self):
    dicePairs = [DicePair(faces=(i+1,j+1)) for j in range(6) for i in range(6)]
    diceGroup = VGroup(*[dicePairs[i] for i in range(36)]).arrange_in_grid(6, 6, buff=0.4).scale(.8).to_edge(LEFT, buff=1.15).shift(.5*DOWN)#.to_corner(UL, buff=.75)

    matches = []
    nColors = [DICE_2, DICE_3, DICE_4, DICE_5, DICE_6, DICE_7, DICE_6, DICE_5, DICE_4, DICE_3, DICE_2]
    for i in range(2,13):
      matches.append(list(filter(lambda dicePair: True if sum(dicePair.faces) == i else False, diceGroup)))
    for i in range(11):
      for j in range(len(matches[i])):
        matches[i][j].set_color(nColors[i])
    self.add(diceGroup)
    txts = [TextMobject(str(7-i), color=nColors[6-i]).scale(.75).next_to(dicePairs[29+i], direction=DOWN) for i in range(1,7)]
    # VGroup(*txts).arrange(RIGHT, buff=1).move_to(diceGroup.get_edge_center(DOWN)+.5*DOWN)
    self.add(*txts)
    setup_board(self)
    boardGroup.to_edge(RIGHT, buff=1.15).shift(.65*UP)#.to_corner(DR, buff=.75)
    coordinatesOfSquares = initialize_coordinates(self)
    self.add(boardGroup)
    player = create_player(self, 18, coordinatesOfSquares)
    player2 = create_player(self, 9, coordinatesOfSquares)
    player3 = create_player(self, 38, coordinatesOfSquares)
    txt = TextMobject("Turns:$\\ \\ 69$").move_to(boardGroup.get_center()).scale(.7)
    txt.set_color_by_gradient(MONOPOLY_RANK_1, MONOPOLY_RANK_8)
    self.add(txt)
    self.add(TextMobject("Illinois Avenue?", color=MONOPOLY_RED).rotate(PI/16).move_to(boardGroup.get_edge_center(DOWN)+.8*DOWN+.15*LEFT).scale(.8))
    self.add(TextMobject("Broadwalk?", color=MONOPOLY_BLUE).rotate(PI/16).move_to(boardGroup.get_edge_center(DOWN)+1.2*DOWN+.75*RIGHT).scale(.8))
    self.add(TextMobject("Winning at Monopoly").scale(1.5).next_to(diceGroup, direction=UP, buff=.6))
