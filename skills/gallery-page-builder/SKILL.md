---
name: gallery-page-builder
description: Create complete photo gallery web pages with lightbox functionality based on a tested template. Use this skill when users want to create a photo gallery webpage, event photo page, trip gallery, portfolio page, or any page displaying multiple images with popup preview. The skill requires headline, subtitle/description, date (optional), and list of image URLs.
---

# Gallery Page Builder

Create professional photo gallery web pages with lightbox popup functionality.

## Template Features

The gallery template includes:
- Responsive grid layout (4 columns desktop, 3 tablet, 2 mobile)
- Lightbox popup with full-screen image preview
- Left/right navigation arrows
- Keyboard navigation (← → ESC)
- Image counter (e.g., "3 / 16")
- Smooth fade animations
- Mobile-friendly responsive design
- Isolated CSS/JS (won't conflict with existing site code)

## Required Input

Gather the following information from the user:

1. **Headline** - Main title for the page
   - Example: "SHANGHAI EXCLUSIVE TRIP Work Hard, Travel Harder."

2. **Subtitle** - Description or context (can be multiple lines)
   - Example: "บันทึกความทรงจำทริปเซี่ยงไฮ้ ทีม Executive Group"

3. **Date** - Optional date or time period
   - Example: "28 - 31 October 2025"
   - Can be omitted if not relevant

4. **Image URLs** - Complete list of all image URLs to display
   - Must be publicly accessible URLs
   - Example format:
     ```
     https://example.com/image1.jpg
     https://example.com/image2.jpg
     https://example.com/image3.jpg
     ```
   - Minimum 1 image, no maximum limit
   - All images should be from the same domain/project for consistency

## Workflow

### Step 1: Collect Information

Ask the user for all required inputs if not already provided. Present them in a clear checklist format:

```
To create your gallery page, I need:

✅ Headline: [provided/needed]
✅ Subtitle: [provided/needed]
⚪ Date: [provided/needed/optional]
✅ Image URLs: [X images provided/needed]

Could you provide [missing items]?
```

### Step 2: Load and Customize Template

1. Read the template file:
   ```bash
   view assets/gallery-template.html
   ```

2. Customize the template by replacing:
   - `<h1>` content with user's Headline
   - First `<p>` in `.pg-header` with user's Subtitle  
   - Second `<p>` in `.pg-header` with user's Date (or remove if not provided)
   - All image URLs in the gallery grid

### Step 3: Generate Image Grid HTML

For each image URL provided, create a gallery item block:

```html
<div class="pg-col">
    <div class="pg-item" data-index="X">
        <img src="IMAGE_URL" alt="Image X">
    </div>
</div>
```

**Important Rules:**
- `data-index` starts from 0 and increments sequentially (0, 1, 2, 3...)
- Use the same URL for both thumbnail `<img src>` and `data-large` attribute
- `alt` text should be "Image X" where X is the image number (1, 2, 3...)

### Step 4: Update Image Data Attributes

In the JavaScript section, update the images array:

```javascript
var images = [
    { src: 'URL1', alt: 'Image 1' },
    { src: 'URL2', alt: 'Image 2' },
    { src: 'URL3', alt: 'Image 3' }
    // ... etc
];
```

### Step 5: Output Complete HTML

Create the complete customized HTML file and save it with an appropriate filename:
- Use the headline to generate a filename
- Convert to lowercase, replace spaces with hyphens
- Example: "Shanghai Trip 2025" → "shanghai-trip-2025.html"

## Example Transformation

**Input:**
```
Headline: SHANGHAI EXCLUSIVE TRIP
Subtitle: บันทึกความทรงจำทริปเซี่ยงไฮ้
Date: 28-31 Oct 2025
Images: 3 URLs provided
```

**Output:** Complete HTML file with:
- Header showing the headline, subtitle, and date
- 3 images in responsive grid
- Lightbox functionality working correctly
- All JavaScript properly configured

## Quality Checklist

Before delivering the final HTML, verify:

✅ All user-provided text is correctly inserted
✅ Image count matches the number of URLs provided
✅ `data-index` attributes are sequential (0, 1, 2, 3...)
✅ JavaScript `images` array matches the HTML image list
✅ No placeholder text remains (e.g., "Image Title", "IMAGE_URL")
✅ File has appropriate filename

## Technical Notes

### Image Requirements

- Images should be publicly accessible URLs
- Recommended size: 500-1200px width for optimal loading
- Supported formats: JPG, PNG, WebP, GIF
- Thumbnails will be automatically fitted to grid (250px height on desktop)

### CSS/JS Isolation

The template uses isolated CSS and JavaScript:
- CSS prefix: `#photo-gallery-component`
- JavaScript namespace: wrapped in IIFE
- Modal moves to `<body>` automatically to prevent z-index issues
- Won't conflict with existing website styles

### Browser Compatibility

- Requires jQuery (1.9+) and Bootstrap 3
- Works on all modern browsers
- Mobile-responsive with touch support
- Keyboard navigation: ← → ESC keys

## Common Customizations

### Change Grid Layout

Modify `.pg-col` width percentages in CSS:
```css
.pg-col {
    width: 25%;  /* 4 columns */
}
```

### Change Background Gradient

Update the gradient in `#photo-gallery-component`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Remove Header Section

Delete or comment out the `.pg-header` section in HTML.

### Change Thumbnail Height

Modify `.pg-item img` height:
```css
.pg-item img {
    height: 250px;  /* default */
}
```

## Troubleshooting

**Images not loading:**
- Verify URLs are publicly accessible
- Check for CORS issues if images are from different domain
- Test URLs in browser directly

**Modal not opening:**
- Ensure jQuery and Bootstrap are loaded before gallery script
- Check browser console for JavaScript errors

**Layout broken:**
- Verify HTML structure is intact
- Check that CSS section is complete
- Ensure no unclosed tags

**Modal behind header:**
- The template automatically moves modal to `<body>`
- If still issues, check header's z-index (should be < 999)

## Output Format

Always create a complete, ready-to-use HTML file:
- Single file with embedded CSS and JavaScript
- No external dependencies except jQuery/Bootstrap (which are CDN-loaded)
- File can be opened directly in browser or uploaded to web server
- Provide download link to user

## Example Usage Patterns

**Simple event gallery:**
```
User: "Create a gallery for my birthday party photos"
→ Ask for: title, description, date, image URLs
→ Generate: birthday-party.html
```

**Business trip gallery:**
```
User: "Make a page for our Shanghai business trip"
→ Ask for: headline, subtitle, dates, image URLs
→ Generate: shanghai-business-trip.html
```

**Portfolio showcase:**
```
User: "I need a portfolio page for my photography"
→ Ask for: title, description, portfolio image URLs
→ Generate: photography-portfolio.html
```
