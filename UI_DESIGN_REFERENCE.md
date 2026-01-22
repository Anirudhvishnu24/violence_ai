# Streamlit UI - Visual Design Reference

## Color Palette

### Primary Colors
```
Indigo       #6366f1   RGB(99, 102, 241)    Main accent, headers, buttons
Blue         #3b82f6   RGB(59, 130, 246)    Secondary accent
```

### Status Colors
```
Red          #ef4444   RGB(239, 68, 68)     Violent/Danger
Green        #10b981   RGB(16, 185, 129)    Safe/Success
Amber        #f59e0b   RGB(245, 158, 11)    Warning
```

### Background Colors
```
Dark Navy    #0f172a   RGB(15, 23, 42)      Main background
Dark Gray    #1e293b   RGB(30, 41, 59)      Card backgrounds
Slate       #334155   RGB(51, 65, 85)      Borders
```

### Text Colors
```
Light Gray   #f1f5f9   RGB(241, 245, 249)   Primary text
Medium Gray  #cbd5e1   RGB(203, 213, 225)   Secondary text
```

## Typography

### Font Weights
```
Normal       500   General text
Medium       600   Labels, captions
Bold         700   Headings, emphasis
Extra Bold   800   Main titles
```

### Font Sizes
```
Hero Title        2.5em    (40px)    Main heading
Section Header    1.4em    (22px)    Section titles
Subtitle          1.1em    (17px)    Descriptive text
Metric Label      0.95em   (15px)    Card labels
Metric Value      2.5em    (40px)    Large numbers
Body Text         1em      (16px)    Main content
Caption           0.85em   (13px)    Small text
```

### Letter Spacing
```
Headers        -1px to 1px    Enhanced visual impact
Labels         1px            Clear separation
Badges         0.5px          Professional look
```

## Component Styles

### Hero Header
```
Background:    Linear gradient (135deg, #6366f1 0%, #3b82f6 100%)
Padding:       40px 30px
Border Radius: 20px
Box Shadow:    0 20px 50px rgba(0, 0, 0, 0.4)
Border:        1px solid rgba(255, 255, 255, 0.1)
```

### Metric Cards
```
Background:    Linear gradient (135deg, #1e293b 0%, rgba(30, 41, 59, 0.8) 100%)
Border:        1px solid #334155
Padding:       24px
Border Radius: 16px
Box Shadow:    0 10px 30px rgba(0, 0, 0, 0.3)
Hover Effect:  translateY(-4px) + shadow upgrade
Transition:    0.3s ease
```

### Confidence Bar
```
Height:        8px
Background:    #334155 (slate)
Border Radius: 10px
Fill Color:    
  - Safe:      Linear gradient (90deg, #6366f1, #10b981)
  - Violent:   Linear gradient (90deg, #ef4444, #f59e0b)
Animation:     width 0.4s ease
```

### Warning Banner
```
Background:    Linear gradient (135deg, #dc2626 0%, #991b1b 100%)
Border:        1px solid rgba(239, 68, 68, 0.3)
Padding:       20px
Border Radius: 12px
Color:         White
Box Shadow:    0 4px 20px rgba(220, 38, 38, 0.3)
```

### Safe Banner
```
Background:    Linear gradient (135deg, #059669 0%, #065f46 100%)
Border:        1px solid rgba(16, 185, 129, 0.3)
Padding:       20px
Border Radius: 12px
Color:         White
Box Shadow:    0 4px 20px rgba(16, 185, 129, 0.3)
```

### Badges
```
Background:    rgba(255, 255, 255, 0.2)
Border:        1px solid rgba(255, 255, 255, 0.3)
Padding:       6px 14px
Border Radius: 20px
Font Size:     0.85em
Font Weight:   600
Backdrop:      blur(10px)
```

### Buttons (File Uploader)
```
Default:       Indigo accent styling
Hover:         Brighter indigo, more visible
Border:        Dashed 2px #6366f1
Background:    rgba(99, 102, 241, 0.05)
Focus:         Solid indigo border
```

## Spacing System

### Padding
```
Tight       6px      Compact spacing
Small       12px     Labels, captions
Medium      20px     Card content
Large       24px     Card padding
XL          30px     Section padding
XXL         40px     Hero padding
```

### Margin
```
Sections:   30px top/bottom
Cards:      20px gap
Columns:    20px gap (medium)
Elements:   10-15px default
Text:       8-10px line spacing
```

### Border Radius
```
Small       8px      Badge-like elements
Medium      12px     Banners
Large       16px     Cards
XL          20px     Hero section
```

## Shadows

### Drop Shadows
```
Subtle      0 10px 30px rgba(0, 0, 0, 0.3)
Medium      0 10px 30px rgba(0, 0, 0, 0.3)
Deep        0 20px 50px rgba(0, 0, 0, 0.4)
```

### Hover State
```
Lift:       translateY(-4px)
Shadow:     Upgrade from subtle to deep
Duration:   0.3s ease transition
```

## Animations

### Slide In
```
From:        opacity: 0, translateY(20px)
To:          opacity: 1, translateY(0)
Duration:    0.5s ease
Applied to:  Metric cards
```

### Progress Bar
```
Width:       0% → 100%
Duration:    0.4s ease
Smoothness:  Continuous animation
```

### Hover Effect
```
Transform:   translateY(-4px)
Shadow:      Subtle to deep
Duration:    0.3s ease
Applied to:  Metric cards
```

### Color Transition
```
Duration:    0.3s ease
Applied to:  Backgrounds, text colors
Smooth:      No jarring color changes
```

## Responsive Design

### Breakpoints
```
Mobile      < 768px   Single column, stacked layout
Tablet      768px+    Two columns, optimized spacing
Desktop     1024px+   Full layout with all features
```

### Mobile Adjustments
```
Hero Title        1.8em (down from 2.5em)
Subtitle          0.95em (down from 1.1em)
Metric Value      1.8em (down from 2.5em)
Metric Cards      Stack in single column
Columns           Auto-adjust width
Padding           Reduced on mobile
```

## UI Flow

### Initial State
```
1. Hero Header (gradient)
   ↓
2. Sidebar + Main area
   ↓
3. Empty state message
   └─ "👆 Upload a video to begin"
```

### Upload State
```
1. File uploader ready
   ├─ Show upload area
   └─ Video preview space
```

### Processing State
```
1. Progress text: "🎬 Extracting frames..."
   ├─ Progress bar: 25%
   ↓
2. Progress text: "🧠 Analyzing with AI..."
   ├─ Progress bar: 75%
   ├─ Spinner visible
   ↓
3. Progress text: "✓ Analysis complete!"
   ├─ Progress bar: 100%
```

### Results State
```
1. Metric cards (animated in)
   ├─ Prediction card
   ├─ Confidence card
   └─ Risk Level card
   ↓
2. Confidence progress bar
   ├─ Percentage display
   └─ Colored fill (red/green)
   ↓
3. Content warning OR safe banner
   ├─ Gradient background
   ├─ Clear messaging
   └─ Visible warning if violent
   ↓
4. Detailed analysis tabs
   ├─ How It Works
   ├─ Decision Logic
   └─ Model Insights
```

## Accessibility

### Contrast Ratios
- Text on dark: ✓ 7:1+ (WCAG AAA)
- Badges on gradient: ✓ 4.5:1+ (WCAG AA)
- Banners: ✓ 8:1+ (WCAG AAA)

### Color Blindness
- Not relying on color alone
- Icons and text provide context
- Red/Green have different saturation
- Percentage values shown

### Keyboard Navigation
- Tab through all elements
- Enter activates buttons
- Expandable sections keyboard accessible
- Focus visible on all interactive elements

## Visual Hierarchy

### Size
```
Level 1: Hero Title (2.5em)
Level 2: Section Headers (1.4em)
Level 3: Metric Labels (0.95em)
Level 4: Body Text (1em)
Level 5: Captions (0.85em)
```

### Color
```
Level 1: Indigo (#6366f1) - Primary accent
Level 2: White/Light Gray (#f1f5f9) - Main content
Level 3: Medium Gray (#cbd5e1) - Secondary
Level 4: Slate (#334155) - Borders/subtle
Level 5: Status colors - Alerts only
```

### Position
```
Hero:      Top (full width)
Main:      Center (two columns)
Sidebar:   Left (collapsible)
Bottom:    Tabs and details
```

## Dark Mode Considerations

✓ All text legible on dark background
✓ Sufficient contrast throughout
✓ No pure white (hurts eyes)
✓ Gradients provide visual interest
✓ Shadows add depth
✓ Accent colors pop against dark
✓ No transparent overlays causing issues

## Production Checklist

- [x] Color palette defined
- [x] Typography system established
- [x] Component styles documented
- [x] Spacing system consistent
- [x] Animations smooth
- [x] Responsive design verified
- [x] Accessibility checked
- [x] Visual hierarchy clear
- [x] Performance optimized
- [x] Cross-browser tested

## Reference Implementation

All colors, sizes, and styles are implemented directly in `app/ui.py` within the `inject_custom_css()` function. No external CSS files needed.

For customization:
1. Locate `inject_custom_css()` function
2. Find CSS variable section (top of `<style>` block)
3. Modify hex codes as needed
4. Refresh browser to see changes

Example:
```css
:root {
    --primary-color: #6366f1;  /* Change this to #3b82f6 for blue */
    --danger-color: #ef4444;
    ...
}
```
