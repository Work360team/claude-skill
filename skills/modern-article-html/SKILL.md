---
name: modern-article-html
description: Create modern, responsive HTML articles with beautiful gradient themes (#667eea to #764ba2) for WordPress/Elementor. Properly converts Markdown to HTML with section dividers (---), auto-generated subtitles, Hero section, Table of Contents, smooth animations, and mobile-responsive design. Use when user requests HTML article creation from markdown files with phrases like "สร้าง HTML สำหรับบทความ" or "แปลง markdown เป็น HTML บทความ".
---

# Modern Article HTML

สร้างไฟล์ HTML บทความสวยงามและทันสมัยที่พร้อมใช้งานใน WordPress Elementor โดยแปลง Markdown เป็น HTML อย่างถูกต้อง

## คุณสมบัติหลัก

- ✨ **Proper Markdown Conversion** - แปลง Markdown เป็น HTML อย่างถูกต้อง
- 📐 **Section Dividers** - รองรับ `---` เป็นตัวแบ่ง section (ไม่แสดงใน HTML)
- 🤖 **Auto-generated Subtitle** - สร้างพาดหัวสั้นๆ จากเนื้อหาอัตโนมัติ
- ✨ **Hero Section** - สวยงามด้วย gradient พื้นหลังและ animation
- 📑 **Table of Contents** - อัตโนมัติจาก headings ระดับ H2
- 🎨 **Gradient Theme** - #667eea → #764ba2 ตลอดทั้งบทความ
- 📊 **Reading Progress Bar** - แสดงความคืบหน้าการอ่านด้านบน
- 🎭 **Smooth Animations** - fade-in เมื่อ scroll
- 📱 **Fully Responsive** - รองรับทุกขนาดหน้าจอ
- 🚀 **Back to Top Button** - เลื่อนกลับด้านบนอย่างลื่นไหล
- 🎯 **No Header/Footer** - เหมาะกับ Elementor และ page builders

## การใช้งาน

### วิธีที่ 1: จากไฟล์ Markdown

เมื่อผู้ใช้มีไฟล์ `.md` และต้องการแปลงเป็น HTML:

```bash
python scripts/md_to_article.py <input-file.md> [output-file.html]
```

**ตัวอย่างคำสั่งจากผู้ใช้:**
- "สร้าง HTML สำหรับบทความ โดยใช้ข้อมูลในไฟล์ claude-skills-explained.md"
- "แปลงไฟล์ my-article.md เป็น HTML สวยๆ"
- "ทำ HTML บทความจากไฟล์ tutorial.md"

**ขั้นตอน:**
1. อ่านไฟล์ markdown ที่ผู้ใช้ระบุ
2. รัน script `md_to_article.py` พร้อมระบุไฟล์ input
3. ได้ไฟล์ HTML พร้อมใช้งาน

**Output ที่ได้:**
- Title: ดึงจาก `# heading` แรก หรือชื่อไฟล์
- Subtitle: สร้างอัตโนมัติจากย่อหน้าแรก (สูงสุด 100 ตัวอักษร)
- Content: แปลง Markdown เป็น HTML อย่างถูกต้อง

### วิธีที่ 2: สร้างจากเนื้อหาโดยตรง

เมื่อผู้ใช้ต้องการให้ Claude เขียนเนื้อหาให้เอง:

```python
from pathlib import Path
import sys
sys.path.append('scripts')
from md_to_article import create_article_html

# สร้างเนื้อหา markdown
content = """
## หัวข้อแรก

เนื้อหาในส่วนแรก...

---

## หัวข้อที่สอง

เนื้อหาในส่วนที่สอง...

### หัวข้อย่อย

รายละเอียดเพิ่มเติม
"""

# สร้าง HTML (subtitle จะถูกสร้างอัตโนมัติ)
html = create_article_html(
    title="หัวข้อบทความ",
    subtitle="",  # เว้นว่างเพื่อสร้างอัตโนมัติ
    content=content
)

# บันทึกไฟล์
with open('article.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

## Markdown Format ที่รองรับ

### Headers

```markdown
# H1 - ใช้เป็น Title เท่านั้น (จะไม่แสดงในเนื้อหา)

## H2 - หัวข้อหลัก (แสดงใน TOC)
### H3 - หัวข้อย่อย
#### H4 - หัวข้อย่อยระดับต่อไป
```

### Text Formatting

```markdown
**ตัวหนา** หรือ __ตัวหนา__
*ตัวเอียง* หรือ _ตัวเอียง_
`inline code`
```

### Section Dividers

```markdown
---
```

เครื่องหมาย `---` จะแบ่ง section ออกเป็นส่วนๆ โดยมีเส้นแบ่งสวยงามพร้อมสัญลักษณ์ ✦

### Code Blocks

```markdown
```python
def hello():
    print("Hello World")
```
```

### Blockquotes

```markdown
> ข้อความพิเศษหรือคำพูดที่ต้องการเน้น
```

### Lists

```markdown
- รายการแบบ bullet
- รายการที่สอง

1. รายการแบบตัวเลข
2. รายการที่สอง
```

### Links และ Images

```markdown
[ข้อความลิงก์](https://example.com)
![คำอธิบายรูป](image.jpg)
```

## การทำงานของ Subtitle อัตโนมัติ

Script จะสร้าง subtitle จากเนื้อหาโดย:

1. ดึงย่อหน้าแรกที่มีความหมาย
2. ลบ Markdown syntax ออก (bold, italic, code, links)
3. ตัดให้เหลือไม่เกิน 100 ตัวอักษร
4. เติม `...` หากข้อความยาวเกินไป

**ตัวอย่าง:**

Markdown:
```markdown
Modern Article HTML Skill เป็นเครื่องมือที่ช่วยให้คุณสร้าง...
```

Subtitle ที่ได้:
```
Modern Article HTML Skill เป็นเครื่องมือที่ช่วยให้คุณสร้าง...
```

## CSS ที่สำคัญ

### CSS บังคับ (รวมเข้ามาเสมอ)

```css
/* Hide ez-toc-container - บังคับซ่อน TOC ของ WordPress */
div#ez-toc-container {
    display: none !important;
}
```

### Section Divider Styling

```css
.section-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #667eea 20%, #764ba2 50%, #667eea 80%, transparent 100%);
    margin: 50px 0;
}
```

มีสัญลักษณ์ ✦ กลางเส้นเพื่อความสวยงาม

### ธีมสี

- **Primary Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Text Color**: `#333` (เนื้อหา), `#555` (ย่อหน้า)
- **Background**: `#f8f9fa` (body), `white` (content boxes)

## ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: แปลงไฟล์ Markdown

```bash
python scripts/md_to_article.py tutorial.md
```

Output:
```
✅ Created: tutorial.html
📊 Size: 16,551 bytes
📝 Title: คู่มือการใช้งาน Python
💬 Subtitle: Python เป็นภาษาโปรแกรมที่ได้รับความนิยมสูงสุด เนื่องจากมีความง่ายในการเรียนรู้...
```

### ตัวอย่างที่ 2: สร้างบทความใหม่

เมื่อผู้ใช้บอก: "สร้าง HTML บทความเรื่อง 'การใช้ Claude AI'"

```python
# 1. เขียนเนื้อหา markdown
content = """
Claude เป็น AI assistant ที่ทรงพลังจาก Anthropic ซึ่งออกแบบมาเพื่อช่วยเหลือในงานต่างๆ

---

## บทนำ

Claude AI สามารถช่วยงานได้หลากหลาย ตั้งแต่การเขียน การวิเคราะห์ ไปจนถึงการเขียนโค้ด

## วิธีการใช้งาน

เริ่มต้นด้วยการสร้าง prompt ที่ชัดเจน

### การสร้าง Prompt

Prompt ที่ดีควรมี:
- ความชัดเจน
- บริบทที่เพียงพอ
- ตัวอย่างที่ดี

---

## สรุป

Claude ช่วยเพิ่มประสิทธิภาพการทำงานได้อย่างมาก
"""

# 2. สร้าง HTML
from md_to_article import create_article_html

html = create_article_html(
    title="การใช้ Claude AI",
    subtitle="",  # จะถูกสร้างอัตโนมัติ
    content=content
)

# 3. บันทึก
with open('/mnt/user-data/outputs/claude-ai-guide.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

## Tips สำหรับผลลัพธ์ที่ดี

1. **ใช้ H2 headings** เป็นหัวข้อหลักเพื่อให้ TOC สมบูรณ์
2. **เขียนย่อหน้าแรกที่ดี** เพราะจะถูกใช้เป็น subtitle
3. **ใช้ --- แบ่ง sections** เพื่อจัดโครงสร้างเนื้อหาให้ชัดเจน
4. **แบ่งเนื้อหาเป็นส่วนๆ** ด้วย headings ที่ชัดเจน
5. **ใช้ blockquotes** สำหรับข้อความสำคัญ
6. **เพิ่มรูปภาพ** เพื่อให้บทความน่าสนใจมากขึ้น

## Responsive Breakpoints

- **Desktop**: > 768px - แสดงเต็มรูปแบบ
- **Tablet**: ≤ 768px - ปรับขนาด font และ padding
- **Mobile**: ≤ 480px - ขนาดกะทัดรัดสำหรับมือถือ

## ไฟล์ที่เกี่ยวข้อง

- `assets/article-template.html` - Template HTML หลัก
- `scripts/md_to_article.py` - Script แปลง Markdown เป็น HTML
