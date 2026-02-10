# backend/io/brd_reader.py
import re
from models.surfboard import SurfboardModel

class BrdReader:
    """
    Parses legacy BoardCAD (.brd) files.
    """
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self.board = SurfboardModel(
            id="imported",
            name="Imported Board",
            dimensions={"length": 0, "width": 0, "thickness": 0},
            outline_points=[],
            rocker_points=[],
            deck_points=[],
            bottom_points=[]
        )

    def parse(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        current_list = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for property lines like "p01 : 195.5"
            prop_match = re.match(r'p(\d+)\s*:\s*(.*)', line)
            if prop_match:
                code = int(prop_match.group(1))
                value = prop_match.group(2)
                self._handle_property(code, value)
                continue

            # Check for start of list "(cp" or end ")"
            if line.startswith('('):
                # Start of a block (Outline, Deck, etc are handled by previous property tags usually, 
                # but in .brd specific p-codes trigger the list read.
                pass 
            
            # Handle Control Points
            # Format: (cp [x,y,cx1,cy1,cx2,cy2] boolean boolean)
            if line.startswith('(cp'):
                self._parse_control_point(line)

        return self.board

    def _handle_property(self, code, value):
        # Map legacy IDs to model
        # 8: Name, 32: Outline, 33: Bottom, 34: Deck
        if code == 8:
            self.board.name = value
        elif code == 32:
            self.current_target = self.board.outline_points
        elif code == 33:
            self.current_target = self.board.bottom_points # For rocker/profile
        elif code == 34:
            self.current_target = self.board.deck_points
        # Note: In a full impl, we would handle all p-codes (1-99)

    def _parse_control_point(self, line):
        # Extract content inside brackets
        match = re.search(r'\[(.*?)\]', line)
        if match and hasattr(self, 'current_target'):
            nums = [float(x) for x in match.group(1).split(',')]
            # Java BrdReader stores 3 points per knot: [Center, Tan1, Tan2]
            # We will store the Center point (first 2 numbers) for the basic shape
            # In a full NURBS implementation, we need all 6 numbers.
            x, y = nums[0], nums[1]
            self.current_target.append((x, y))

def parse_brd(file_path) -> SurfboardModel:
    reader = BrdReader(file_path)
    return reader.parse()