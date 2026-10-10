import os
import http.server
import socketserver
import webbrowser

# --------------------------
# 公共样式
# --------------------------
common_style = """
<style>
    /* 基础极简风格样式 */
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 0; color: #333; background-color: #fafafa; line-height: 1.6; }
    a { text-decoration: none; color: inherit; }
    
    /* 顶部导航栏 */
    header { background-color: #571801; color: #fff; padding: 20px 50px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100;}
    header h1 { margin: 0; font-size: 24px; font-weight: 400; letter-spacing: 3px; text-transform: uppercase; }
    header h1 a { color: #fff; transition: opacity 0.3s; }
    header h1 a:hover { opacity: 0.8; }
    nav a { color: #ccc; text-decoration: none; margin-left: 20px; font-size: 13px; text-transform: uppercase; transition: color 0.3s;}
    nav a:hover { color: #fff; }
    .lang-switch { background: transparent; border: 1px solid #ccc; color: #ccc; padding: 5px 12px; margin-left: 20px; cursor: pointer; transition: all 0.3s;}
    .lang-switch:hover { border-color: #fff; color: #fff; }
    
    /* 首屏区域 - 加入背景图与半透明黑色遮罩 */
    .hero { 
        height: 50vh; 
        display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; 
        /* 修改下面 url 中的 'bg.jpg' 为您的实际图片文件名 */
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('photos/主页背景图.jpg') no-repeat center center;
        background-size: cover;
    }
    /* 首屏文字改为白色，并加入轻微阴影以保证在复杂背景图上清晰可读 */
    .hero h2 { font-size: 42px; margin: 0; font-weight: 300; letter-spacing: 2px; color: #fff; text-shadow: 1px 1px 5px rgba(0,0,0,0.6); }
    .hero p { font-size: 16px; color: #f0f0f0; margin-top: 15px; letter-spacing: 1px; text-shadow: 1px 1px 5px rgba(0,0,0,0.6); }
    
    /* 通用板块 */
    .section { padding: 80px 50px; max-width: 1100px; margin: 0 auto; }
    .section h3 { font-size: 24px; font-weight: 300; text-transform: uppercase; margin-bottom: 40px; letter-spacing: 1px; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
    
    /* 主页卡片网格 - 调整为整块可点击 */
    .grid { display: flex; gap: 30px; flex-wrap: wrap; }
    .card-link { flex: 1 1 300px; text-decoration: none; color: inherit; display: block; }
    .card { background: #fff; padding: 30px; height: 100%; box-sizing: border-box; box-shadow: 0 4px 10px rgba(0,0,0,0.03); transition: transform 0.3s, box-shadow 0.3s; border-top: 3px solid transparent;}
    .card-link:hover .card { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.08); border-top: 3px solid #571801; }
    .card h4 { margin-top: 0; font-size: 20px; padding-bottom: 15px; color: #571801; margin-bottom: 15px; font-weight: 400;}
    .card p { font-size: 14px; color: #666; margin-bottom: 20px;}
    .card .more { font-size: 13px; color: #571801; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }
    
    footer { background: #571801; color: #ddd; text-align: center; padding: 30px; font-size: 12px; margin-top: 50px; }
</style>
"""

# --------------------------
# 公共头部导航（按照新顺序排列）
# --------------------------
def build_header(current_page):
    # 顺序：首页、简介、项目、媒体、曲目、日程、联系
    nav_list = [
        ("home", "Home 首页", "index.html"),
        ("about", "Biography 简介", "about.html"),
        ("media", "Media 媒体", "media.html"),
        ("projects", "Projects 项目", "projects.html"),
        ("schedule", "Schedule 日程", "schedule.html"),
        ("contact", "Contact 联系", "contact.html"),
    ]
    nav_html = ""
    for key, text, href in nav_list:
        style = 'style="color: #fff; border-bottom: 1px solid #fff; padding-bottom: 2px;"' if key == current_page else ''
        nav_html += f'            <a href="{href}" {style}>{text}</a>\n'
    
    return f"""
<header>
    <h1><a href="index.html">Shen Jinyu 申晋宇</a></h1>
    <nav>
{nav_html}
        
    </nav>
</header>
"""

common_footer = """
<footer>
    <p>&copy; 2026 Shen Jinyu. All Rights Reserved.</p>
</footer>
"""

# --------------------------
# 生成各个页面内容
# --------------------------

# 首页 index.html (按照新顺序排列卡片)
index_html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>申晋宇 Shen Jinyu | Conductor 指挥</title>{common_style}</head><body>{build_header("home")}
    <div class="hero">
        <h2>Shen Jinyu 申晋宇</h2>
        <p>Conductor 青年指挥 | 个人官方网站</p>
    </div>
    <div class="section">
        <div class="grid">
            <a href="about.html" class="card-link">
                <div class="card">
                    <h4>Biography 个人简介</h4>
                    <p>了解申晋宇的教育背景、职业生涯发展以及在古典音乐领域取得的成就摘要。</p>
                    <span class="more">点击进入预览 →</span>
                </div>
            </a>
            <a href="media.html" class="card-link">
                <div class="card">
                    <h4>Media 媒体资料</h4>
                    <p>浏览演出现场的视频录像和排练剧照。</p>
                    <span class="more">点击进入预览 →</span>
                </div>
            </a>
            <a href="projects.html" class="card-link">
                <div class="card">
                    <h4>Projects 艺术企划</h4>
                        <p>了解申晋宇创立的艺术项目。</p>
                    <span class="more">点击进入预览 →</span>
                </div>
             </a>
            <a href="schedule.html" class="card-link">
                <div class="card">
                    <h4>Schedule 演出日程</h4>
                    <p>查看即将到来的音乐会、歌剧演出计划以及过往演出的精彩回顾。</p>
                    <span class="more">点击进入预览 →</span>
                </div>
            </a>
            <a href="contact.html" class="card-link">
                <div class="card">
                    <h4>Contact 联系方式</h4>
                    <p>获取联络信息，进行演出邀约、媒体采访及商务合作沟通。</p>
                    <span class="more">点击进入预览 →</span>
                </div>
            </a>
        </div>
    </div>
{common_footer}</body></html>"""

# 其他详细子页面
about_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biography 简介 | 申晋宇 Shen Jinyu</title>
    {common_style}
    <style>
        .bio-header {{ text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid #eaeaea; }}
        .bio-header h2 {{ margin: 0; font-size: 28px; color: #571801; letter-spacing: 2px; }}
        .bio-header p {{ color: #666; font-size: 14px; margin-top: 8px; }}

        /* 新增的个人照片样式 */
        .bio-image {{ text-align: center; margin-bottom: 40px; }}
        .bio-image img {{ 
            max-width: 100%; 
            height: auto; 
            max-height: 400px; /* 控制照片的最大高度 */
            border-radius: 4px; /* 轻微圆角 */
            box-shadow: 0 8px 20px rgba(0,0,0,0.08); /* 轻微阴影增加高级感 */
            object-fit: cover;
        }}

        .bio-content {{ display: flex; flex-direction: column; gap: 35px; }}
        .bio-section h4 {{ font-size: 18px; color: #571801; border-left: 4px solid #571801; padding-left: 10px; margin-bottom: 15px; font-weight: 500; }}
        .bio-text p {{ margin-bottom: 15px; text-align: justify; font-size: 15px; line-height: 1.8; color: #444; }}
        .bio-list {{ list-style-type: none; padding: 0; margin: 0; }}
        .bio-list li {{ margin-bottom: 10px; font-size: 15px; color: #444; position: relative; padding-left: 15px; }}
        .bio-list li::before {{ content: "•"; color: #571801; position: absolute; left: 0; font-weight: bold; }}
        .ensemble-list {{ column-count: 2; column-gap: 40px; list-style-type: none; padding: 0; margin: 0; }}
        .ensemble-list li {{ margin-bottom: 8px; font-size: 14px; color: #555; position: relative; padding-left: 15px; break-inside: avoid; }}
        .ensemble-list li::before {{ content: "•"; color: #ccc; position: absolute; left: 0; }}
        @media (max-width: 768px) {{ .ensemble-list {{ column-count: 1; }} }}
    </style>
</head>
<body>
    {build_header("about")}
    <div class="section">
        <h3>Biography | 个人简介</h3>
        
        <div class="bio-header">
            <h2>申晋宇 Shen Jinyu</h2>
            <p>旅德青年指挥 | Conductor</p>
        </div>

        <!-- 新增的照片展示区域 -->
        <div class="bio-image">
            <!-- 请确认图片路径，这里假设照片名为“个人照片.jpg”并存放在 photos 文件夹内 -->
            <img src="photos/个人简介.jpg" alt="申晋宇 Shen Jinyu 个人照片">
        </div>
        
        <div class="bio-content">
            <div class="bio-section">
                <h4>Current Positions | 现任职务</h4>
                <ul class="bio-list">
                    <li>CANTO室内合唱团艺术总监 (Artistic Director, CANTO vocal ensemble)</li>
                    <li>AIR 现代乐集首席指挥 (Principal Conductor, AIR Contemporary Music Collective)</li>
                    <li>爱乐佳合青少年合唱团指挥 (Conductor, Aiyue Jiahe Youth Choir)</li>
                    <li>东岸音乐实验学校指挥教师 (Conducting Teacher, Beijing Eastbank Music of Academy )</li>
                </ul>
            </div>
            
            <div class="bio-section bio-text">
                <h4>Education Background | 教育背景</h4>
                <p>本科毕业于中央音乐学院指挥系并保送研究生，师从夏小汤教授、郑小瑛教授。辅修录音艺术指导专业并获得毕业证书。求学期间曾荣获中国国家奖学金。随后旅德就读于德国国立罗伯特舒曼音乐学院 (Robert Schumann Hochschule Düsseldorf) 学习指挥和钢琴，以满分成绩毕业并获硕士学位。</p>
                <p>留德期间师从著名德国指挥家、教育家 Rüdiger Bohn 教授与 Christian von Gehren 教授，并随 Timo Nuoranne 教授辅修合唱指挥。曾参加吕嘉、Jorma Panula、Ulrich Windfuhr 等著名音乐家的大师班，并获得高度评价。</p>
                <p>She graduated with a Bachelor`s degree from the Conducting Department of the Central Conservatory of Music and was directly admitted to postgraduate study, where she studied under Professors Xia Xiaotang and Zheng Xiaoying. She also minored in Recording Art Direction with a certification of completion. During her studies, she was awarded the China National Scholarship. She was also  studied conducting and piano at the Robert Schumann Hochschule Düsseldorf, Germany, graduating with a Master`s degree and achieving the highest marks.</p>
                <p>While in Germany, she studied under the renowned German conductor and educator Prof. Rüdiger Bohn and Prof. Christian von Gehren, and took a minor in choral conducting under Prof. Timo Nuoranne. She participated in masterclasses led by renowned musicians such as Lü Jia, Jorma Panula and Ulrich Windfuhr, receiving high praise.</p>
            </div>
            
            <div class="bio-section bio-text">
                <h4>Professional Experience | 职业经历</h4>
                <p>曾任中国爱乐乐团青少年交响乐团指挥、北京理工大学合唱团指挥。在德国期间，曾担任埃森交响乐团 (Essener Symphonie Orchester)、埃森青年交响乐团 (Essener Jugend Symphonie Orchester) 和下萨克森州青年爱乐乐团 (Jungend Philharmonisches Orchester Niedersachsen) 的助理指挥。在歌剧与清唱剧领域，她曾在《艺术家的生涯》(La Bohème)、《蝴蝶夫人》(Madame Butterfly)、《托斯卡》(Tosca)、《女人心》(Così fan tutte)、《创世纪》(Die Schöpfung)、《以利亚》(Elias)、《风流寡妇》(Die lustige Witwe) 及《伤逝》等项目中担任助理指挥和合唱指挥。</p>
                <p>作为 AIR 现代乐集 (AIR Contemporary Music Collective) 首席指挥，自乐团 2018 年成立以来,成功首演数十部现代作品及室内乐歌剧,并执棒杭州现代音乐节等重要演出。2025年起任教于北京市东岸音乐学校,担任指挥专业助教和合唱课教师,策划并成功上演多场专题音乐会。</p>
                <p>She has served as conductor of the China Philharmonic Youth Symphony Orchestra and the Beijing Institute of Technology Choir. Whilst in Germany, she served as assistant conductor for Essener Symphonie Orchester, Essener Jugend Symphonie Orchester and Jungend Philharmonisches Orchester Niedersachsen. In the field of opera and oratorio, she has conducted <i>La Bohème</i>, <i>Madame Butterfly</i>, <i>Tosca</i>, <i>Così fan tutte</i>, <i>Die Schöpfung</i>, <i>Elias</i>, <i>Die lustige Witwe</i>.</p>
                <p>As Principal Conductor of the AIR Contemporary Music Collective, she has, since the ensemble`s founding in 2018, successfully premiered dozens of contemporary works and chamber operas, and has conducted major performances such as the Hangzhou Contemporary Music Festival. Since 2025, she started teaching at the Beijing Eastbank Music of Academy, serving as a teaching assistant in the conducting programme and a choral teacher, whilst also organising and performing numerous concerts.</p>
            </div>

            <div class="bio-section">
                <h4>Collaborations | 合作乐团与合唱团</h4>
                <ul class="ensemble-list">
                    <li>杜塞尔多夫交响乐团 (Düsseldorfer Symphoniker)</li>
                    <li>威斯特法伦爱乐乐团 (Westfalen Neue Philharmonie)</li>
                    <li>莱茵爱乐乐团 (Rheinische Philharmonie)</li>
                    <li>杜伊斯堡爱乐乐团 (Duisburger Philharmoniker)</li>
                    <li>西德室内交响乐团 (Südwestdeutsches Kammerorchester)</li>
                    <li>埃森爱乐乐团 (Essen Philharmonie)</li>
                    <li>罗马尼亚 Dinu Lipatti 交响乐团 (Filarmonica Dinu Lipatti)</li>
                    <li>罗伯特舒曼交响乐团 (Sinfonieorchester der RSH)</li>
                    <li>当代乐团 (Musikfabrik Ensemble)</li>
                    <li>下萨克森青年爱乐乐团 (Jungend Philharmonisches Orchester Niedersachsen)</li>
                    <li>中国青年交响乐团</li>
                    <li>RSH Vokalensemble</li>
                    <li>Candomino 合唱团</li>
                    <li>兰州音乐厅合唱团</li>
                </ul>
            </div>
        </div>
    </div>
    {common_footer}
</body>
</html>"""

# 媒体页 media.html
media_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media 媒体 | 申晋宇 Jinyu Shen</title>
    {common_style}
    <style>
        /* 媒体页专属样式 */
        .media-section-title {{ font-size: 20px; color: #571801; margin-bottom: 20px; border-bottom: 2px solid #571801; display: inline-block; padding-bottom: 5px; }}
        
        /* 视频容器 */
        .video-grid {{ display: flex; flex-direction: column; gap: 40px; margin-bottom: 60px; }}
        .video-item {{ width: 100%; max-width: 800px; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background: #000; }}
        .video-item video {{ width: 100%; display: block; }}
        .video-caption {{ text-align: center; font-size: 14px; color: #666; margin-top: 10px; }}

        /* 照片瀑布流/网格 */
        .photo-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .photo-item {{ width: 100%; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
        .photo-item img {{ width: 100%; height: auto; display: block; transition: transform 0.3s ease; }}
        .photo-item:hover img {{ transform: scale(1.03); }}
    </style>
</head>
<body>
    {build_header("media")}
    
    <div class="section">
        <h3>Media | 媒体资料</h3>
        
        <!-- 视频部分 -->
        <h4 class="media-section-title">Videos 视频</h4>
        <div class="video-grid">
            <!-- 视频 1  -->
            <div>
                <div class="video-item">
                    <video controls poster="photos/申晋宇 Der fliegende Holländer.png">
                        <source src="videos/申晋宇 Der fliegende Holländer.mp4" type="video/mp4">
                    </video>
                </div>
                <p class="video-caption">Der fliegende Holländer - R.Wagner</p>
            </div>

            <!-- 视频 2 -->
            <div>
                <div class="video-item">
                    <video controls poster="photos/申晋宇 Boulez Memoriale.png">
                        <source src="videos/申晋宇 Boulez Memoriale.mp4" type="video/mp4">
                    </video>
                </div>
                <p class="video-caption">Memoriale - P.Boulez</p>
            </div>

            <!-- 视频 3 -->
            <div>
                <div class="video-item">
                    <video controls poster="photos/Blessed are the dead.png">
                        <source src="videos/Blessed are the dead.mp4" type="video/mp4">
                    </video>
                 </div>
                <p class="video-caption">Blessed are the dead - H.Howells</p>
            </div>
        </div>

        

        <!-- 照片部分 -->
        <h4 class="media-section-title">Photos 照片</h4>
        <div class="photo-grid">
            <!-- 照片 1 -->
            <div class="photo-item">
                <!-- 请确保照片文件与生成的 HTML 处于同级目录的 photos 文件夹中，或修改这里的路径 -->
                <img src="photos/照片1-1.jpg" alt="Concert Photo 1">
            </div>
            <!-- 照片 2 -->
            <div class="photo-item">
                <img src="photos/照片1-2.jpg" alt="Concert Photo 2">
            </div>
            <!-- 照片 3 -->
            <div class="photo-item">
                <img src="photos/照片1-3.jpg" alt="Concert Photo 3">
            </div>
            <!-- 照片 4 -->
            <div class="photo-item">
                <img src="photos/照片2-1.jpg" alt="Concert Photo 4">
            </div>
            <!-- 照片 5 -->
            <div class="photo-item">
                <img src="photos/照片2-2.jpg" alt="Concert Photo 5">
            </div>
            <!-- 照片 6 -->
            <div class="photo-item">
                <img src="photos/照片2-3.jpg" alt="Concert Photo 6">
            </div>
            <!-- 照片 7 -->
            <div class="photo-item">
                <img src="photos/照片3-1.jpg" alt="Concert Photo 7">
            </div>
            <!-- 照片 8 -->
            <div class="photo-item">
                <img src="photos/照片3-2.jpg" alt="Concert Photo 8">
            </div>
            <!-- 照片 9 -->
            <div class="photo-item">
                <img src="photos/照片3-3.jpg" alt="Concert Photo 9">
            </div>
        </div>
    </div>
    
    {common_footer}
</body>
</html>"""

projects_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projects 项目 | 申晋宇 Jinyu Shen</title>
    {common_style}
    <style>
        /* 新增的 Headline 样式 (参照简介页) */
        .page-header {{ text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid #eaeaea; }}
        .page-header h2 {{ margin: 0; font-size: 28px; color: #571801; letter-spacing: 2px; }}
        .page-header p {{ color: #666; font-size: 14px; margin-top: 8px; }}

        /* 新增：项目主页链接按钮样式 */
        .project-link {{ display: inline-block; margin-top: 15px; font-size: 14px; color: #571801; text-decoration: none; font-weight: bold; transition: opacity 0.3s; border: 1px solid #571801; padding: 6px 15px; border-radius: 4px; }}
        .project-link:hover {{ background-color: #571801; color: #fff; }}

        /* 图文排版样式：使用 flexbox 实现左图右文 */
        .project-card {{ display: flex; gap: 30px; margin-bottom: 50px; align-items: flex-start; }}
        .project-logo {{ flex: 0 0 325px; }}
        .project-logo img {{ width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
        .project-info {{ flex: 1; /* 右侧文字占据剩余所有空间 */ }}
        .project-info h4 {{ font-size: 22px; color: #571801; border-left: 4px solid #571801; padding-left: 10px; margin-bottom: 15px; font-weight: 500; }}
        .project-info p {{ margin-bottom: 15px; text-align: justify; font-size: 15px; line-height: 1.8; color: #444; }}
        
        
        /* 手机端自适应适配 */
        @media (max-width: 768px) {{
            .project-card {{ flex-direction: column; align-items: center; text-align: center; gap: 20px; }}
            .project-logo {{ width: 120px; flex: auto; }}
        }}

    </style>
</head>
<body>
    {build_header("projects")}
    <div class="section">
        <h3>Projects | 艺术企划</h3>

        <div class="project-card">
            <div class="project-logo">
                <!-- 请确认 CANTO 合唱团的 logo 图片路径 -->
                <img src="photos/canto.jpg" alt="CANTO Vocal Ensemble Logo">
            </div>
            <div class="project-info">
                <h4>CANTO Vocal Ensemble | CANTO室内合唱团</h4>
                <p>申晋宇创办的CANTO青年室内合唱团是立足北京的新锐室内合唱团体,专注演绎多风格合唱作品。合唱团秉持回归人声本质的艺术理念,兼顾古典作品的庄重质感与当代作品的多元风格。以专业化、年轻化为发展方向，致力于打造高质量的室内合唱艺术平台。未来，团队将持续推出专场音乐会、专题展演及原创作品展示等艺术活动，深耕室内合唱领域，持续传播多元的合唱艺术。</p>
                <p>The CANTO Vocal Ensemble is a chamber choir founded by Shen Jinyu, based in Beijing, specialising in the performance of choral works across a variety of styles. Upholding an artistic philosophy centred on  the essence of the individual artistic voice. In the future, the ensemble will continue to organise chroal concerts, commissioned works concerts , deepening its engagement with the field of chamber choir whilst continuing to promote the diversity of choral art.</p>
                <a href="https://xhslink.cn/o/ATZX9F3uFBm" target="_blank" class="project-link">访问主页 / Visit Homepage →</a>
            </div>
        </div>

        <div class="project-card" style="margin-bottom: 0;">
            <div class="project-logo">
                <!-- 请确认 大耳青年 的 logo 图片路径 -->
                <img src="photos/大耳青年.jpg" alt="大耳青年 Podcast Logo">
            </div>
            <div class="project-info">
                <h4>Podcast | 大耳青年</h4>
                <p>申晋宇创办的《大耳青年》是一档访谈与分享的播客，与不同专业背景的朋友们谈论音乐和艺术。我们邀请各行各业的朋友们坐下对谈，围绕音乐、艺术与生活展开交流。在对话中，倾听不同职业背景的人分享与艺术相伴的真实体验、思考与选择。</p>
                <p>This is a podcast programm featuring interviews and discussions, where we talk about music and the arts with friends from diverse professional backgrounds.</p>
                <a href="https://www.xiaoyuzhoufm.com/podcast/634ea974fc1737df59631e0a" target="_blank" class="project-link">收听播客 / Listen to Podcast →</a>
            </div>
        </div>
    </div>
    {common_footer}
</body>
</html>"""

schedule_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Schedule 日程 | 申晋宇 Shen Jinyu</title>
    {common_style}
    <style>
        /* 新增的 Headline 样式 (参照简介页) */
        .page-header {{ text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid #eaeaea; }}
        .page-header h2 {{ margin: 0; font-size: 28px; color: #571801; letter-spacing: 2px; }}
        .page-header p {{ color: #666; font-size: 14px; margin-top: 8px; }}
        
        /* 日程页专属样式 */
        .schedule-container {{ max-width: 800px; margin: 0 auto; padding-top: 20px; }}
        
        .schedule-year {{ 
            font-size: 28px; 
            color: #571801; 
            border-bottom: 2px solid #571801; 
            padding-bottom: 10px; 
            margin-top: 60px; 
            margin-bottom: 30px; 
            font-weight: 300; 
            letter-spacing: 2px;
        }}
        .schedule-year:first-child {{ margin-top: 0; }}
        
        .schedule-item {{ 
            display: flex; 
            border-bottom: 1px solid #eaeaea; 
            padding: 25px 15px; 
            transition: background-color 0.3s ease; 
        }}
        .schedule-item:hover {{ background-color: #f5f0ed; }}
        
        .schedule-date {{ 
            flex: 0 0 150px; 
            font-weight: 500; 
            color: #333; 
            font-size: 18px; 
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }}
        
        .schedule-info {{ flex: 1; }}
        .schedule-title {{ font-size: 18px; color: #111; margin: 0 0 8px 0; font-weight: 500; }}
        .schedule-ensemble {{ font-size: 15px; color: #666; margin: 0; }}
        
        /* 手机端适配：屏幕较小时日期和演出信息改为上下排列 */
        @media (max-width: 600px) {{
            .schedule-item {{ flex-direction: column; padding: 20px 10px; }}
            .schedule-date {{ margin-bottom: 12px; font-size: 16px; color: #571801; }}
        }}
    </style>
</head>
<body>
    {build_header("schedule")}
    <div class="section">
        <h3 style="text-align: center; margin-bottom: 60px;">Concerts | 音乐会日程</h3>
        
        <div class="schedule-container">
            
            <!-- 2026 年日程 -->
            <div class="schedule-year">2026</div>
            
            <div class="schedule-item">
                <div class="schedule-date">2026.12.24</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">专场音乐会</h4>
                    <p class="schedule-ensemble">CANTO & BEAM 合唱团</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2026.09.06</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">腾讯浪潮音乐大赏</h4>
                    <p class="schedule-ensemble">嘉兴大潮爱乐乐团</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2026.07.07</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">红墙杯合唱比赛</h4>
                    <p class="schedule-ensemble">财政部机关合唱团</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2026.06.18</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">专场音乐会</h4>
                    <p class="schedule-ensemble">BEAM合唱团</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2026.01.15</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">冬日音乐会</h4>
                    <p class="schedule-ensemble">BEAM合唱团</p>
                </div>
            </div>

            <!-- 2025 年日程 -->
            <div class="schedule-year">2025</div>
            
            <div class="schedule-item">
                <div class="schedule-date">2025.07.13</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">专场音乐会</h4>
                    <p class="schedule-ensemble">RSH-Vokalensemble</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2025.07.04</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">钢琴独奏音乐会</h4>
                    <p class="schedule-ensemble">Solo Recital</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2025.06.07</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">专场音乐会</h4>
                    <p class="schedule-ensemble">Westfalen Neue Philharmonie 交响乐团</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2025.05.17</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">Boulez纪念音乐会</h4>
                    <p class="schedule-ensemble">RSH-Ensemble</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2025.04.06</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">专场音乐会</h4>
                    <p class="schedule-ensemble">Candomino 合唱团</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2025.02.21</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">专场音乐会</h4>
                    <p class="schedule-ensemble">Dinu Lipatti 交响乐团</p>
                </div>
            </div>
            
            <div class="schedule-item">
                <div class="schedule-date">2025.01.24</div>
                <div class="schedule-info">
                    <h4 class="schedule-title">专场音乐会</h4>
                    <p class="schedule-ensemble">RSH-Vokalensemble</p>
                </div>
            </div>

        </div>
    </div>
    {common_footer}
</body>
</html>"""

# 联系页 contact.html
contact_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact 联系 | 申晋宇 ShenJinyu</title>
    {common_style}
    <style>
        .contact-container {{ max-width: 600px; margin: 0 auto; text-align: center; padding: 50px 30px; }}
        .contact-item {{ margin-bottom: 30px; font-size: 16px; }}
        .contact-item span.title {{ display: block; font-size: 14px; color: #571801; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }}
        .contact-item a {{ color: #333; transition: color 0.3s; }}
        .contact-item a:hover {{ color: #571801; text-decoration: underline; }}
    </style>
</head>
<body>
    {build_header("contact")}
    <div class="section">
        <h3>Contact | 联系方式</h3>
        <div class="card contact-container" style="text-align: left; padding: 40px 50px;">
            
            <div class="contact-item" style="margin-bottom: 35px; font-size: 20px;">
                <span class="title" style="display: block; font-size: 18px; color: #571801; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">Email / 电子邮箱</span>
                <p style="margin: 10px 0;"><a href="mailto:shenjinyu952@gmail.com" style="color: #333; text-decoration: none;">shenjinyu952@gmail.com</a></p>
                <p style="margin: 10px 0;"><a href="mailto:shenjinyumusic@qq.com" style="color: #333; text-decoration: none;">shenjinyumusic@qq.com</a></p>
            </div>
            
            <div class="contact-item" style="margin-bottom: 35px; font-size: 20px;">
                <span class="title" style="display: block; font-size: 18px; color: #571801; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">Phone / 联系电话</span>
                <p style="margin: 10px 0;"><a href="tel:+8618600239010" style="color: #333; text-decoration: none;">+86 186 0023 9010</a></p>
            </div>

            <div class="contact-item" style="margin-bottom: 10px; font-size: 20px;">
                <span class="title" style="display: block; font-size: 18px; color: #571801; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">Social Media / 社交媒体</span>
                <p style="margin: 15px 0;">
                    <!-- 这里是带图标的 Instagram 超链接 -->
                    <a href="https://www.instagram.com/jinyu_shen_?psln=MWJkZnE5bG0wc3NwZQ%3D%3D&utm_source=qr" target="_blank" style="color: #333; text-decoration: none; display: inline-flex; align-items: center; transition: color 0.3s;" onmouseover="this.style.color='#571801'" onmouseout="this.style.color='#333'">
                        
                        <!-- 极简 Instagram SVG 图标 -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px;">
                            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                            <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                            <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                        </svg>
                        
                        <span style="font-size: 20px;">@jinyu_shen_</span>
                    </a>
                </p>
            </div>
            
        </div>
    </div>
    {common_footer}
</body>
</html>"""

# --------------------------
# 批量写入与服务器启动
# --------------------------
pages = {
    "index.html": index_html, 
    "about.html": about_html, 
    "projects.html": projects_html,  # 新增的页面
    "schedule.html": schedule_html,
    "media.html": media_html, 
    "contact.html": contact_html,
}

for filename, content in pages.items():
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已生成: {filename}")

class FastRequestHandler(http.server.SimpleHTTPRequestHandler):
    def address_string(self):
        host, port = self.client_address[:2]
        return host

PORT = 8000
try:
    with socketserver.ThreadingTCPServer(("", PORT), FastRequestHandler) as httpd:
        print(f"\n🌐 优化版服务器已启动！访问: http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()
except OSError:
    print(f"\n⚠️ 端口 {PORT} 占用，请尝试直接在浏览器打开 index.html。")