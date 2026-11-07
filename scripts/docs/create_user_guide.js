const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  ImageRun, PageBreak, Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign, Header, Footer, PageNumber, LevelFormat
} = require('docx');

const projectRoot = path.resolve(__dirname, '../..');
const outDir = path.join(projectRoot, 'artifacts/user-guide');
fs.mkdirSync(outDir, { recursive: true });

function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function svgShell(body, title) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="900" viewBox="0 0 1500 900">
  <rect width="1500" height="900" fill="#f4f6f8"/>
  <rect x="0" y="0" width="1500" height="58" fill="#714b67"/><text x="30" y="37" font-family="Arial" font-size="25" fill="white" font-weight="700">Sean Music</text>
  <rect x="0" y="58" width="250" height="842" fill="#252b35"/><text x="24" y="105" font-family="Arial" font-size="20" fill="#e7e9ed">Bán hàng</text><text x="24" y="157" font-family="Arial" font-size="18" fill="#bdc5cf">Đơn báo giá</text><text x="24" y="200" font-family="Arial" font-size="18" fill="#bdc5cf">Đơn bán hàng</text><text x="24" y="243" font-family="Arial" font-size="18" fill="#bdc5cf">Giao hàng</text><text x="24" y="286" font-family="Arial" font-size="18" fill="#bdc5cf">Sản phẩm</text>
  <rect x="285" y="92" width="1170" height="72" rx="4" fill="white" stroke="#d9dee5"/><text x="315" y="136" font-family="Arial" font-size="28" fill="#222" font-weight="700">${esc(title)}</text>
  ${body}
  <text x="30" y="878" font-family="Arial" font-size="14" fill="#9aa3ad">Ảnh minh họa thao tác · Sean Music</text>
  </svg>`;
}
function text(x,y,t,size=18,fill='#333',weight='400') { return `<text x="${x}" y="${y}" font-family="Arial" font-size="${size}" fill="${fill}" font-weight="${weight}">${esc(t)}</text>`; }
function field(x,y,w,label,value,ring=false) { return `<text x="${x}" y="${y}" font-family="Arial" font-size="15" fill="#666">${esc(label)}</text><rect x="${x}" y="${y+12}" width="${w}" height="38" rx="3" fill="white" stroke="#cbd2d9"/><text x="${x+12}" y="${y+37}" font-family="Arial" font-size="17" fill="#333">${esc(value)}</text>${ring?`<ellipse cx="${x+w/2}" cy="${y+31}" rx="${w/2+12}" ry="${33}" fill="none" stroke="#e3262e" stroke-width="5"/>`:''}`; }
async function makeImages() {
  const sale = svgShell(`
    <rect x="285" y="185" width="1170" height="650" rx="4" fill="white" stroke="#d9dee5"/>
    <rect x="320" y="212" width="132" height="42" rx="4" fill="#714b67"/><text x="351" y="239" font-family="Arial" font-size="17" fill="white" font-weight="700">Xác nhận</text><rect x="467" y="212" width="115" height="42" rx="4" fill="#eef0f3"/><text x="494" y="239" font-family="Arial" font-size="17" fill="#555">Gửi báo giá</text>
    <text x="1195" y="241" font-family="Arial" font-size="18" fill="#714b67" font-weight="700">Bản nháp</text>
    ${field(330,285,470,'Khách hàng','Khách hàng mẫu Sean Music')}
    ${field(850,285,260,'Nhân viên bán hàng','Nguyễn Nhường Em')}
    ${field(1135,285,260,'Cộng tác viên','Nguyễn Nhường Em',true)}
    ${field(330,390,470,'Ngày đặt hàng','22/09/2026')}
    ${field(850,390,260,'Tham chiếu khách hàng','SEAN-MUSIC-001')}
    ${field(1135,390,260,'Hoa hồng','170.000 ₫',true)}
    <text x="330" y="500" font-family="Arial" font-size="20" fill="#333" font-weight="700">Dòng đơn hàng</text>
    <rect x="330" y="525" width="1065" height="42" fill="#eef0f3"/><text x="350" y="552" font-family="Arial" font-size="16" fill="#555">Sản phẩm</text><text x="880" y="552" font-family="Arial" font-size="16" fill="#555">Số lượng</text><text x="1040" y="552" font-family="Arial" font-size="16" fill="#555">Đơn giá</text><text x="1270" y="552" font-family="Arial" font-size="16" fill="#555">Thành tiền</text>
    <rect x="330" y="567" width="1065" height="58" fill="white" stroke="#e3e6ea"/><text x="350" y="603" font-family="Arial" font-size="16" fill="#333">Beat nhạc độc quyền - Gói Basic</text><text x="900" y="603" font-family="Arial" font-size="16" fill="#333">2</text><text x="1040" y="603" font-family="Arial" font-size="16" fill="#333">500.000 ₫</text><text x="1270" y="603" font-family="Arial" font-size="16" fill="#333">1.000.000 ₫</text>
    <rect x="330" y="625" width="1065" height="58" fill="white" stroke="#e3e6ea"/><text x="350" y="661" font-family="Arial" font-size="16" fill="#333">Dịch vụ mix &amp; master - Gói Standard</text><text x="900" y="661" font-family="Arial" font-size="16" fill="#333">1</text><text x="1040" y="661" font-family="Arial" font-size="16" fill="#333">1.200.000 ₫</text><text x="1270" y="661" font-family="Arial" font-size="16" fill="#333">1.200.000 ₫</text>
    <text x="1120" y="760" font-family="Arial" font-size="18" fill="#555">Tổng tiền chưa thuế</text><text x="1270" y="760" font-family="Arial" font-size="20" fill="#222" font-weight="700">2.200.000 ₫</text>
    <path d="M 800 275 C 980 245, 1110 230, 1190 275" fill="none" stroke="#e3262e" stroke-width="4"/><text x="1180" y="205" font-family="Arial" font-size="16" fill="#e3262e" font-weight="700">1. Chọn CTV</text>
    <path d="M 1410 440 C 1380 470, 1370 500, 1360 525" fill="none" stroke="#e3262e" stroke-width="4"/><text x="1230" y="475" font-family="Arial" font-size="16" fill="#e3262e" font-weight="700">2. Kiểm tra hoa hồng</text>
    <path d="M 455 210 C 470 175, 550 175, 590 210" fill="none" stroke="#e3262e" stroke-width="4"/><text x="600" y="198" font-family="Arial" font-size="16" fill="#e3262e" font-weight="700">3. Xác nhận đơn</text>
  `, 'Đơn bán hàng SO0001');
  const delivery = svgShell(`
    <rect x="285" y="185" width="1170" height="650" rx="4" fill="white" stroke="#d9dee5"/>
    <rect x="320" y="212" width="100" height="42" rx="4" fill="#714b67"/><text x="342" y="239" font-family="Arial" font-size="17" fill="white" font-weight="700">Xác nhận</text><rect x="435" y="212" width="128" height="42" rx="4" fill="#eef0f3"/><text x="465" y="239" font-family="Arial" font-size="17" fill="#555">In phiếu</text>
    <text x="1170" y="241" font-family="Arial" font-size="18" fill="#2a7b42" font-weight="700">Sẵn sàng</text>
    <text x="330" y="315" font-family="Arial" font-size="17" fill="#666">Tham chiếu</text><text x="330" y="342" font-family="Arial" font-size="20" fill="#222" font-weight="700">SO0001</text>
    <text x="700" y="315" font-family="Arial" font-size="17" fill="#666">Khách hàng</text><text x="700" y="342" font-family="Arial" font-size="20" fill="#222">Khách hàng mẫu Sean Music</text>
    <text x="330" y="405" font-family="Arial" font-size="20" fill="#333" font-weight="700">Hoạt động giao hàng</text>
    <rect x="330" y="430" width="1065" height="48" fill="#eef0f3"/><text x="350" y="461" font-family="Arial" font-size="16" fill="#555">Sản phẩm</text><text x="900" y="461" font-family="Arial" font-size="16" fill="#555">Yêu cầu</text><text x="1060" y="461" font-family="Arial" font-size="16" fill="#555">Đã xử lý</text><text x="1250" y="461" font-family="Arial" font-size="16" fill="#555">Đơn vị</text>
    <rect x="330" y="478" width="1065" height="58" fill="white" stroke="#e3e6ea"/><text x="350" y="514" font-family="Arial" font-size="16" fill="#333">Beat nhạc độc quyền - Gói Basic</text><text x="910" y="514" font-family="Arial" font-size="16" fill="#333">2</text><text x="1070" y="514" font-family="Arial" font-size="16" fill="#333">0</text><text x="1250" y="514" font-family="Arial" font-size="16" fill="#333">cái</text>
    <rect x="330" y="536" width="1065" height="58" fill="white" stroke="#e3e6ea"/><text x="350" y="572" font-family="Arial" font-size="16" fill="#333">Dịch vụ mix &amp; master - Gói Standard</text><text x="910" y="572" font-family="Arial" font-size="16" fill="#333">1</text><text x="1070" y="572" font-family="Arial" font-size="16" fill="#333">0</text><text x="1250" y="572" font-family="Arial" font-size="16" fill="#333">dịch vụ</text>
    <rect x="330" y="680" width="1065" height="64" rx="4" fill="#fff7e6" stroke="#e7b65c"/><text x="355" y="720" font-family="Arial" font-size="17" fill="#7a5400">Kiểm tra số lượng thực tế trước khi bấm Xác nhận</text>
    <ellipse cx="370" cy="233" rx="65" ry="35" fill="none" stroke="#e3262e" stroke-width="5"/><text x="325" y="190" font-family="Arial" font-size="16" fill="#e3262e" font-weight="700">1. Mở phiếu giao</text>
    <ellipse cx="1185" cy="233" rx="130" ry="32" fill="none" stroke="#e3262e" stroke-width="5"/><text x="1110" y="180" font-family="Arial" font-size="16" fill="#e3262e" font-weight="700">2. Kiểm tra trạng thái</text>
    <path d="M 1410 720 C 1390 700, 1380 670, 1360 620" fill="none" stroke="#e3262e" stroke-width="4"/><text x="1180" y="650" font-family="Arial" font-size="16" fill="#e3262e" font-weight="700">3. Kiểm hàng</text>
  `, 'Phiếu giao hàng WH/OUT/0001');
  const status = svgShell(`
    <rect x="285" y="185" width="1170" height="650" rx="4" fill="white" stroke="#d9dee5"/>
    <text x="330" y="245" font-family="Arial" font-size="25" fill="#222" font-weight="700">Đơn bán hàng</text>
    <rect x="330" y="285" width="1065" height="74" rx="4" fill="#eef6ff"/><text x="365" y="330" font-family="Arial" font-size="19" fill="#225b89" font-weight="700">Đã xác nhận</text><text x="720" y="330" font-family="Arial" font-size="19" fill="#225b89">→ Đang giao</text><text x="1080" y="330" font-family="Arial" font-size="19" fill="#225b89">→ Đã giao</text>
    <rect x="330" y="405" width="500" height="160" fill="#fafbfc" stroke="#d9dee5"/><text x="360" y="445" font-family="Arial" font-size="17" fill="#666">Đơn bán hàng</text><text x="360" y="480" font-family="Arial" font-size="26" fill="#222" font-weight="700">SO0001</text><text x="360" y="525" font-family="Arial" font-size="16" fill="#555">Trạng thái: Đã xác nhận</text>
    <rect x="875" y="405" width="520" height="160" fill="#fafbfc" stroke="#d9dee5"/><text x="905" y="445" font-family="Arial" font-size="17" fill="#666">Giao hàng</text><text x="905" y="480" font-family="Arial" font-size="26" fill="#222" font-weight="700">WH/OUT/0001</text><text x="905" y="525" font-family="Arial" font-size="16" fill="#2a7b42" font-weight="700">Trạng thái: Đã giao</text>
    <rect x="330" y="620" width="1065" height="80" rx="4" fill="#eaf7ee" stroke="#8fc99f"/><text x="365" y="670" font-family="Arial" font-size="18" fill="#246b39">Hoàn tất: đơn đã xác nhận và phiếu giao đã được xử lý.</text>
    <path d="M 330 320 C 500 300, 650 295, 810 320" fill="none" stroke="#e3262e" stroke-width="5"/><text x="340" y="285" font-family="Arial" font-size="16" fill="#e3262e" font-weight="700">Theo dõi luồng trạng thái</text>
    <ellipse cx="1135" cy="485" rx="240" ry="100" fill="none" stroke="#e3262e" stroke-width="5"/><text x="1120" y="610" font-family="Arial" font-size="16" fill="#e3262e" font-weight="700">Xác nhận phiếu đã giao</text>
  `, 'Theo dõi trạng thái xử lý');
  const items = [['01_tao_don.png',sale],['02_xu_ly_giao_hang.png',delivery],['03_kiem_tra_trang_thai.png',status]];
  for (const [name, svg] of items) await sharp(Buffer.from(svg)).png().toFile(path.join(outDir,name));
}

const red = 'E3262E', purple = '714B67', gray = '666666';
function p(text, opts={}) { return new Paragraph({spacing:{after:120,line:1.15}, ...opts, children:[new TextRun({text, font:'Arial', size:22, color:'222222', ...opts.run})]}); }
function bullet(text) { return new Paragraph({style:'List Bullet', spacing:{after:70}, children:[new TextRun({text, font:'Arial', size:22})]}); }
function heading(text, level=1) { return new Paragraph({heading: level===1?HeadingLevel.HEADING_1:HeadingLevel.HEADING_2, spacing:{before:220,after:120}, children:[new TextRun({text, font:'Arial', bold:true, color:'000000'})]}); }
function caption(text) { return new Paragraph({alignment:AlignmentType.CENTER, spacing:{after:160}, children:[new TextRun({text, font:'Arial', size:18, italics:true, color:gray})]}); }
function img(file,w=6.45) { return new Paragraph({alignment:AlignmentType.CENTER, spacing:{before:80,after:60}, children:[new ImageRun({data:fs.readFileSync(path.join(outDir,file)), transformation:{width:w*96,height:w*96*0.6}, type:'png'})]}); }
function step(n,title,body) { return new Paragraph({spacing:{after:80}, children:[new TextRun({text:`Bước ${n} · ${title}`,font:'Arial',bold:true,size:23,color:purple}), new TextRun({text:`\n${body}`,font:'Arial',size:22,color:'222222'})]}); }
function table(rows) { return new Table({width:{size:100,type:WidthType.PERCENTAGE}, borders:{top:{style:BorderStyle.SINGLE,size:6,color:'D9D9D9'},bottom:{style:BorderStyle.SINGLE,size:6,color:'D9D9D9'},left:{style:BorderStyle.SINGLE,size:6,color:'D9D9D9'},right:{style:BorderStyle.SINGLE,size:6,color:'D9D9D9'},insideH:{style:BorderStyle.SINGLE,size:6,color:'D9D9D9'},insideV:{style:BorderStyle.SINGLE,size:6,color:'D9D9D9'}}, rows:rows.map((r,i)=>new TableRow({children:r.map(c=>new TableCell({width:{size:100/r.length,type:WidthType.PERCENTAGE},shading:i===0?{type:ShadingType.CLEAR,fill:purple}:undefined,verticalAlign:VerticalAlign.CENTER,children:[new Paragraph({spacing:{after:50},children:[new TextRun({text:c,font:'Arial',size:20,bold:i===0,color:i===0?'FFFFFF':'222222'})]})]}))}))}); }

async function main(){
  await makeImages();
  const doc = new Document({styles:{default:{document:{run:{font:'Arial',size:22,color:'222222'},paragraph:{spacing:{line:1.15}}}},title:{run:{font:'Arial',bold:true,color:'000000',size:36},paragraph:{spacing:{after:180}}},heading1:{run:{font:'Arial',bold:true,color:'000000',size:28},paragraph:{spacing:{before:260,after:140,keepNext:true}}},heading2:{run:{font:'Arial',bold:true,color:'000000',size:24},paragraph:{spacing:{before:180,after:100,keepNext:true}}}},sections:[{properties:{page:{margin:{top:720,right:720,bottom:720,left:720}}},headers:{default:new Header({children:[new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:'SEAN MUSIC · HƯỚNG DẪN VẬN HÀNH',font:'Arial',size:16,color:'666666'})]})]})},footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:'Trang ',font:'Arial',size:16,color:'666666'}),new TextRun({children:[PageNumber.CURRENT],font:'Arial',size:16,color:'666666'})]})]})},children:[
    new Paragraph({style:'Title',alignment:AlignmentType.CENTER,children:[new TextRun({text:'Hướng Dẫn Sử Dụng Bán Hàng Và Xử Lý Vận Chuyển',font:'Arial',bold:true,size:34,color:'000000'})]}),
    new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:200},children:[new TextRun({text:'Dành cho user thao tác trên hệ thống Sean Music',font:'Arial',size:23,color:gray})]}),
    new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:280},children:[new TextRun({text:'Phiên bản 1.0 · 22/09/2026',font:'Arial',size:18,color:'888888'})]}),
    img('01_tao_don.png',5.9),
    new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:260},children:[new TextRun({text:'Mục tiêu: tạo đúng đơn, xác nhận đúng thời điểm và hoàn tất xử lý giao hàng.',font:'Arial',size:21,bold:true,color:purple})]}),
    heading('Phạm vi hướng dẫn',1),
    p('Tài liệu mô tả luồng thao tác cơ bản của user bán hàng trên Odoo/Sean Music: tạo đơn bán hàng, gán cộng tác viên, xác nhận đơn, mở phiếu giao hàng, kiểm tra số lượng và cập nhật trạng thái hoàn tất.'),
    table([['Vai trò','Thao tác chính'],['User bán hàng','Tạo đơn, nhập khách hàng/sản phẩm, chọn cộng tác viên, xác nhận đơn'],['User xử lý vận chuyển','Mở phiếu giao, kiểm tra số lượng thực tế, xác nhận giao hàng'],['Quản lý','Theo dõi trạng thái đơn và số tiền hoa hồng đã ghi nhận']]),
    heading('Quy trình tổng quát',1),
    p('Thực hiện theo thứ tự: Đơn bán hàng → Xác nhận → Phiếu giao hàng → Kiểm hàng → Xác nhận giao → Kiểm tra trạng thái.'),
    new Paragraph({children:[new TextRun({text:'Lưu ý về ảnh: ',font:'Arial',size:21,bold:true,color:red}),new TextRun({text:'các ảnh trong tài liệu là ảnh minh họa bố cục thao tác của hệ thống; vị trí nút/trường cần đối chiếu với màn hình thật nếu giao diện được cấu hình khác.',font:'Arial',size:21})]}),
    new Paragraph({children:[new PageBreak()]}),
    heading('1. Tạo đơn bán hàng',1),
    p('Vào menu Bán hàng → Đơn bán hàng → Tạo. Nhập đầy đủ thông tin trước khi xác nhận.'),
    step(1,'Chọn khách hàng','Chọn đúng khách hàng nhận hàng/dịch vụ. Kiểm tra tên và thông tin liên hệ trước khi tiếp tục.'),
    step(2,'Chọn cộng tác viên','Tại trường Cộng tác viên, chọn người được hưởng hoa hồng cho đơn này. Đây là trường bổ sung của Sean Music.'),
    step(3,'Thêm sản phẩm','Trong Dòng đơn hàng, chọn sản phẩm, nhập số lượng và kiểm tra đơn giá.'),
    step(4,'Kiểm tra hoa hồng','Kiểm tra trường Hoa hồng sau khi chọn cộng tác viên và sản phẩm. Mức hoa hồng có thể thay đổi theo quy tắc sản phẩm.'),
    step(5,'Xác nhận đơn','Chỉ bấm Xác nhận khi khách hàng, sản phẩm, số lượng và giá trị đơn đã đúng. Sau khi xác nhận, đơn chuyển khỏi trạng thái Nháp.'),
    img('01_tao_don.png',6.45), caption('Hình 1. Vùng khoanh đỏ: Cộng tác viên, Hoa hồng và nút Xác nhận.'),
    new Paragraph({children:[new TextRun({text:'Điểm kiểm tra trước khi xác nhận: ',font:'Arial',size:21,bold:true}),new TextRun({text:'(1) khách hàng đúng; (2) sản phẩm và số lượng đúng; (3) cộng tác viên đúng; (4) giá/chiết khấu đúng; (5) hoa hồng hiển thị hợp lý.',font:'Arial',size:21})]}),
    new Paragraph({children:[new PageBreak()]}),
    heading('2. Xử lý vận chuyển',1),
    p('Sau khi đơn bán hàng được xác nhận, hệ thống tạo hoặc liên kết phiếu giao hàng. Mở phiếu giao từ nút Giao hàng trên đơn hoặc menu Bán hàng → Giao hàng.'),
    step(1,'Mở phiếu giao hàng','Mở phiếu có tham chiếu đến đơn bán hàng, ví dụ WH/OUT/0001.'),
    step(2,'Kiểm tra trạng thái','Chỉ xử lý các phiếu ở trạng thái Sẵn sàng hoặc tương đương. Nếu phiếu còn Nháp, kiểm tra lại đơn bán hàng và tồn kho.'),
    step(3,'Đối chiếu hàng thực tế','So sánh sản phẩm, số lượng yêu cầu và số lượng thực tế đóng gói. Với dịch vụ, xác nhận nội dung đã hoàn thành.'),
    step(4,'Xác nhận giao hàng','Bấm Xác nhận sau khi số lượng thực tế đã đúng. Nếu giao thiếu, nhập số lượng thực tế và xử lý phần còn lại theo quy định nội bộ.'),
    img('02_xu_ly_giao_hang.png',6.45), caption('Hình 2. Vùng khoanh đỏ: nút xử lý, trạng thái phiếu và khu vực kiểm hàng.'),
    new Paragraph({children:[new TextRun({text:'Không bấm Xác nhận khi chưa kiểm hàng thực tế. ',font:'Arial',size:21,bold:true,color:red}),new TextRun({text:'Thao tác này làm thay đổi trạng thái giao hàng và có thể ảnh hưởng đến tồn kho/báo cáo.',font:'Arial',size:21})]}),
    new Paragraph({children:[new PageBreak()]}),
    heading('3. Kiểm tra trạng thái và hoa hồng',1),
    p('Sau khi xử lý, mở lại đơn bán hàng để kiểm tra trạng thái giao hàng. Với đơn có cộng tác viên, kiểm tra số hoa hồng đã được ghi nhận theo chính sách của hệ thống.'),
    step(1,'Kiểm tra trạng thái đơn','Đơn phải thể hiện đã xác nhận; phiếu giao liên quan phải ở trạng thái đã giao/hoàn tất.'),
    step(2,'Đối chiếu phiếu giao','Mở liên kết phiếu giao để chắc chắn tham chiếu đúng đơn, đúng khách hàng và đã xử lý đủ số lượng.'),
    step(3,'Đối chiếu hoa hồng','Kiểm tra trường Hoa hồng trên đơn hoặc báo cáo hoa hồng. Giá trị được tính theo kế hoạch và quy tắc sản phẩm.'),
    img('03_kiem_tra_trang_thai.png',5.75), caption('Hình 3. Vùng khoanh đỏ: chuỗi trạng thái và kết quả giao hàng.'),
    heading('4. Xử lý tình huống thường gặp',1),
    table([['Tình huống','Cách xử lý'],['Không thấy cộng tác viên','Kiểm tra user có quyền và cộng tác viên đã được tạo/kích hoạt.'],['Hoa hồng bằng 0 hoặc chưa đúng','Kiểm tra cộng tác viên, kế hoạch hoa hồng và quy tắc theo sản phẩm; không tự sửa sau khi đã xác nhận nếu chưa được phân quyền.'],['Không thấy phiếu giao hàng','Kiểm tra đơn đã được xác nhận chưa và sản phẩm có cấu hình giao hàng hay không.'],['Giao thiếu hàng','Nhập số lượng thực tế; không xác nhận đủ số lượng nếu hàng chưa giao. Báo quản lý để xử lý phần còn lại.'],['Bấm nhầm Xác nhận','Dừng thao tác tiếp theo và báo quản lý để kiểm tra khả năng điều chỉnh theo quyền được cấp.']]),
    heading('5. Checklist nhanh',1),
    bullet('Khách hàng và thông tin giao nhận đúng.'), bullet('Sản phẩm, số lượng, đơn giá và tổng tiền đúng.'), bullet('Cộng tác viên được chọn đúng; hoa hồng đã được kiểm tra.'), bullet('Đơn đã xác nhận trước khi xử lý giao hàng.'), bullet('Số lượng thực tế đã đối chiếu trước khi xác nhận phiếu giao.'), bullet('Đơn và phiếu giao hiển thị trạng thái hoàn tất sau cùng.'),
  ]}]
  });
  const file = path.join(outDir,'Huong_dan_su_dung_ban_hang_va_xu_ly_van_chuyen.docx');
  fs.writeFileSync(file, await Packer.toBuffer(doc));
  console.log(file);
}
main().catch(e=>{console.error(e);process.exit(1)});
