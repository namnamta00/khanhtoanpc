# Khánh Toàn Computer — Studio Fanpage

## Bản mới nhất: mẫu bài bán hàng

Mở [KhanhToanStudio.exe](dist/StudioMau/KhanhToanStudio/KhanhToanStudio.exe). Bản này thay thế StudioText và giữ các tính năng trước.

Bài mới có tiêu đề in hoa kèm emoji, các ý nổi bật bắt đầu bằng ✅, giá nếu có, chữ ký cửa hàng cố định và hashtag cuối bài. Website, hotline, hai địa chỉ được chèn nguyên văn theo mẫu người dùng cung cấp. Mẫu không AI dùng từng dòng mô tả làm một ý; nên nhập mỗi đặc điểm trên một dòng. AI viết lại phần sản phẩm theo cùng bố cục và chỉ được dùng dữ liệu nhập. Bài cũ cần tạo lại để áp dụng mẫu mới.

## Bản cập nhật nội dung bài đăng

Mở bản mới tại [KhanhToanStudio.exe](dist/StudioText/KhanhToanStudio/KhanhToanStudio.exe). Các đường dẫn StudioMedia/StudioMoi bên dưới là bản trước.

AI được yêu cầu chỉ trả nội dung bài đăng; ứng dụng lọc các lời dẫn đầu bài như “Tuyệt vời! Dưới đây là bài viết…” trước khi hiển thị và lưu. Bài đã tạo trước đó cần tạo lại hoặc xóa lời dẫn thủ công.

Model mặc định theo cấu hình người dùng: GPT viết bài `gpt-5.6-terra`, tạo ảnh `gpt-image-2.5-flare`; Gemini viết bài `gemini-2.5-flash`, tạo ảnh `gemini-2.5-flash-image`. Có thể sửa trong tab Kết nối. Chưa kiểm chứng quyền truy cập các model bằng API key thật.

## Chẩn đoán lỗi Facebook HTTP 400

Bản `dist/StudioMedia/KhanhToanStudio/KhanhToanStudio.exe` đã hiển thị bước thất bại, mã lỗi Meta, mã phụ, thông báo đã ẩn token và mã tra cứu. HTTP 400 riêng lẻ không đủ xác định lỗi token, quyền hay media.

Vào **Kết nối → Kiểm tra fanpage** trước: thao tác chỉ đọc thông tin, không đăng bài. Nếu lỗi, chụp thông báo chi tiết để kiểm tra; không gửi Page Access Token. Nếu kiểm tra thành công nhưng đăng thất bại, xem bước trong thông báo (tải ảnh / đăng video / xuất bản bài). Trước khi thử đăng lại, kiểm tra trang để tránh bài trùng.

## Danh sách media có tích chọn và kéo thả

Bản mới: `dist/StudioMedia/KhanhToanStudio/KhanhToanStudio.exe`.

Trong tab **Ảnh & video**, ảnh/video vừa tạo xuất hiện trong một danh sách có ảnh thu nhỏ, số thứ tự và ô tích chọn. Có thể thêm PNG/JPG/WEBP/MP4 từ máy qua **Thêm ảnh / video từ máy**. Giữ biểu tượng **☰** rồi kéo tới dòng đích (viền xanh), thả chuột để đổi thứ tự; cũng có thể dùng **↑ ↓**. Cuộn tự động khi kéo sát mép danh sách. Các mục giữ nguyên trạng thái tích khi di chuyển.

**Kiểm tra & đăng các mục đã chọn** lấy bản chụp danh sách đang tích, theo thứ tự từ trên xuống. Hộp xác nhận liệt kê file và nội dung trước khi gửi. Chọn toàn ảnh: một bài văn bản + các ảnh đã chọn theo thứ tự gửi; chọn đúng một video: video + nội dung mô tả. Không tích mục nào: hộp xác nhận ghi rõ chỉ đăng văn bản. Các file không tích không được tải lên.

**Giới hạn bản tích hợp hiện tại:** chưa hỗ trợ một bài trộn ảnh + video hoặc nhiều video. Ứng dụng chặn kiểu lựa chọn này trước khi gọi Facebook; không tự bỏ media hay tách thành nhiều bài. Chưa xác minh bằng tài khoản thật rằng Meta hỗ trợ kiểu bài trộn. Thứ tự gửi ảnh được giữ, nhưng bố cục hiển thị do Facebook quyết định.

**Xuất các mục đã chọn theo thứ tự** tạo thư mục mới, chép nguyên file đã chọn với tiền tố `001_`, `002_`..., kèm nội dung và danh sách thứ tự JSON. Có thể dùng để đăng thủ công; thứ tự hiển thị cuối cùng cần kiểm tra trên Facebook. Xuất không đăng bài và không thay đổi file gốc.

Tạo bộ media mới sẽ thay danh sách cũ bằng bộ vừa tạo. Chỉ tạo lại văn bản sẽ giữ danh sách và lựa chọn hiện có; cần duyệt lại trước khi đăng. Danh sách hiện giữ trong phiên app, chưa tự khôi phục khi đóng/mở.

Các hướng dẫn “Bài viết kèm ảnh” / “Video đang chọn” dưới đây dành cho bản cũ; bản mới tự xác định từ các ô tích chọn.

## Giao diện mới — nhập sản phẩm trực tiếp

Mở `dist/StudioMoi/KhanhToanStudio/KhanhToanStudio.exe`. Tab **Soạn nội dung** có tên sản phẩm (bắt buộc), mô tả ban đầu và giá bán (tùy chọn). Không cần CSV/Excel. Nếu không nhập giá, bài mẫu bỏ phần giá; yêu cầu AI cũng hướng dẫn bỏ giá.

Nhập yêu cầu thêm nếu muốn, chọn GPT/Gemini rồi bấm **Tạo văn bản**. Tắt **Dùng AI viết bài** để thử bài mẫu không cần số dư API. Kết quả có thể sửa, sao chép và lưu. Không tự đăng Facebook.

Tab **Ảnh & video** chứa media tùy chọn và thao tác đăng Facebook; tab **Kết nối** chứa API key/model/token. Đây là bản giao diện bo góc mới; các đường dẫn và hướng dẫn CSV ở các mục phía dưới chỉ áp dụng cho bản cũ.

## Thử chỉ tạo văn bản

Mở bản `dist/chi-tao-text/KhanhToanStudio/KhanhToanStudio.exe`. Nhập báo giá, chọn sản phẩm, bổ sung mô tả rồi bấm **CHỈ TẠO VĂN BẢN — KHÔNG ĐĂNG FACEBOOK**. Nút này đặt số ảnh/video bằng 0 và tắt tạo ảnh AI; không gọi Facebook hoặc yêu cầu token trang.

Mặc định **Dùng AI viết bài** tắt: tạo bài mẫu tiếng Việt từ báo giá, không cần API key. Bật tùy chọn này nếu muốn GPT/Gemini viết bài và đã có khóa với hạn mức phù hợp. Chỉ tạo văn bản bằng GPT vẫn sử dụng API tính phí; không khắc phục lỗi `credit_balance_exhausted`.

Kết quả hiện bên phải, có thể sửa và bấm **Lưu bài đã sửa**. Không bấm nút đăng Facebook khi chỉ thử nội dung. Không có thao tác tự đăng sau khi tạo.

## Bản sửa lỗi HTTP 429

Bản sửa nằm tại `dist/ban-sua-loi/KhanhToanStudio/KhanhToanStudio.exe` để không thay thế ứng dụng đang mở.

OpenAI HTTP 429 có thể là hết số dư/hạn mức API hoặc vượt tốc độ yêu cầu. Bản mới đọc mã lỗi để hướng dẫn tương ứng; nếu máy chủ không trả mã rõ ràng, ứng dụng báo chưa xác định, không tự kết luận thiếu tiền. Kiểm tra Billing và Limits của đúng project trên OpenAI Platform. Không cần bật quyền Videos để tạo slideshow vì video được dựng trên máy.

Nếu tạo ảnh/video lỗi sau khi đã viết bài, bản mới giữ nội dung và media đã hoàn thành để xem, lưu và mở thư mục kết quả. Nếu bước viết bài AI lỗi, tác vụ dừng và giữ nguyên bản đang sửa. Có thể tắt cả hai tùy chọn AI để tạo nội dung mẫu, ảnh quảng cáo và slideshow mà không gọi API.

## Mở ứng dụng

Chạy `dist/KhanhToanStudio/KhanhToanStudio.exe`. Khi chuyển sang máy Windows khác, sao chép **cả thư mục KhanhToanStudio**, không chỉ file exe. Bản đóng gói dành cho Windows cùng kiến trúc với máy build.

1. Mở báo giá Excel `.xlsx` hoặc CSV, chọn một sản phẩm.
2. Nhập mô tả bổ sung, số ảnh (0–10), số video (0–5). Chọn ảnh thật của sản phẩm nếu có.
3. Bấm tạo bài. Sửa nội dung, kiểm tra giá/thông số, xem ảnh và mở video bằng nhấp đúp.
4. Trong **Kết nối & hướng dẫn**, nhập cấu hình Facebook. Kiểm tra tên fanpage trước khi đăng.
5. Chọn đăng bài kèm ảnh hoặc một video, bấm kiểm tra & đăng, xác nhận trang nhận bài.

Kết quả lưu tại `Documents/KhanhToanStudio` trong thư mục người dùng. Nút Lưu bài đã sửa lưu nội dung hiện tại. Mỗi lần tạo dùng thư mục mới; các bản cũ vẫn được giữ.

## Báo giá

Xem [báo giá mẫu](bao_gia_mau.csv). Đọc sheet đầu tiên của Excel. Cột bắt buộc: `Tên sản phẩm` (hoặc `Tên hàng`, `Sản phẩm`, `Name`). Cột tùy chọn: `Giá`, `Mô tả`, `Mã sản phẩm`. Tìm dòng tiêu đề trong 30 dòng đầu. Excel có công thức cần mở và lưu bằng Excel để có giá trị tính sẵn. PDF, ảnh chụp báo giá và `.xls` chưa được hỗ trợ.

## Nội dung, ảnh và video

### Chọn GPT / OpenAI hoặc Gemini

Chọn dịch vụ ở màn hình soạn bài hoặc tab **Kết nối & hướng dẫn**. Các ô API key, model viết nội dung và model tạo ảnh tự chuyển sang cấu hình của dịch vụ đã chọn, giữ riêng các giá trị trong phiên chạy.

- **GPT / OpenAI** (mặc định): nhập OpenAI API key hoặc đặt biến môi trường `OPENAI_API_KEY`. Model viết bài mặc định `gpt-4.1-mini`, model ảnh `gpt-image-1`; có thể nhập model khác mà tài khoản được phép sử dụng. Model văn bản phải hỗ trợ Responses API; model ảnh dùng GPT Image và trả ảnh base64 qua Images API.
- **Gemini**: nhập Gemini API key hoặc đặt `GEMINI_API_KEY`, dùng các model Gemini trong các ô tương ứng.
- Bật **Dùng AI viết bài** và/hoặc **Dùng AI tạo ảnh minh họa**. Nếu không bật, ứng dụng dùng nội dung mẫu và thẻ quảng cáo cục bộ, không gọi AI.
- Dữ liệu được gửi đến đúng nhà cung cấp đã chọn. API key không được lưu vào file. Cần API key có quyền và hạn mức; ứng dụng không dùng phiên đăng nhập ChatGPT trên trình duyệt.

Tích hợp OpenAI dựa trên [hướng dẫn tạo văn bản](https://developers.openai.com/api/docs/guides/text) và [Images API](https://developers.openai.com/api/reference/resources/images/methods/generate). Kiểm thử dùng phản hồi giả lập, chưa xác minh yêu cầu trả phí bằng API key thật.

- Không bật AI: nội dung mẫu tiếng Việt và hashtag được tạo từ thông tin báo giá. Ảnh là thẻ quảng cáo 1080×1080, có ảnh gốc khi bạn chọn; ứng dụng không tự tìm ảnh sản phẩm trên Internet.
- Bật AI viết bài: gửi thông tin sản phẩm và mô tả bổ sung đến OpenAI hoặc Gemini đã chọn. Cần Internet, API key và hạn mức phù hợp.
- Bật AI tạo ảnh: tạo ảnh minh họa theo tên/thông tin sản phẩm bằng dịch vụ đã chọn. Hình có thể khác sản phẩm thật; ảnh gốc đã chọn chỉ được dùng ở chế độ thẻ quảng cáo. Kiểm tra ảnh trước khi đăng. Model có thể thay đổi; tên model nhập được trong ứng dụng.
- Video MP4 H.264 720×720 là slideshow có hiệu ứng phóng nhẹ, 3 giây/ảnh, không âm thanh hoặc giọng đọc. Nhiều video đổi thứ tự ảnh; khi chỉ có một ảnh, video sẽ giống nhau. Nếu số ảnh bằng 0 nhưng có video, ứng dụng tạo một ảnh nội bộ để dựng video.
- Tạo media/AI chạy nền để giao diện vẫn thao tác được. Lỗi giữa chừng có thể để lại media đã hoàn thành trong thư mục kết quả.

## Cấu hình Facebook

Đường dẫn trang mục tiêu: https://www.facebook.com/khanhtoancomputer . Đường dẫn này **không thay thế Page ID và token**.

1. Dùng tài khoản có quyền quản lý trang, tạo/cấu hình ứng dụng tại https://developers.facebook.com/ .
2. Trong luồng đăng nhập/công cụ Meta phù hợp, cấp `pages_manage_posts` và `pages_read_engagement`; `pages_show_list` cần cho bước lấy danh sách trang. Các quyền phụ thuộc cấu hình ứng dụng và yêu cầu hiện hành của Meta.
3. Lấy Page ID và **Page Access Token** của chính fanpage này, nhập ở tab Kết nối. Không dùng token của trang khác hoặc chỉ User Access Token.
4. Bấm kiểm tra token: ứng dụng kiểm tra `/me` khớp Page ID, hiện tên và liên kết trang để bạn đối chiếu.
5. Phiên bản API mặc định `v24.0`, có thể đổi theo phiên bản đang được ứng dụng Meta hỗ trợ. Khi mở cho người ngoài vai trò phát triển, Meta có thể yêu cầu App Review, quyền nâng cao và xác minh doanh nghiệp.

Ảnh được tải lên ở trạng thái chưa xuất bản, rồi gắn vào một bài feed. Video được gửi riêng qua endpoint videos; chưa hỗ trợ Reels hoặc lên lịch. Nếu mạng đứt sau khi gửi, kiểm tra trang trước khi thử lại để tránh đăng trùng. Media tải lên trước khi một yêu cầu sau đó lỗi có thể còn trên Meta ở trạng thái chưa xuất bản.

Token/API key chỉ nằm trong bộ nhớ phiên chạy, không lưu trong file cấu hình. Có thể truyền bằng biến môi trường `FACEBOOK_PAGE_ID`, `FACEBOOK_PAGE_TOKEN`, `GEMINI_API_KEY`. API key Gemini lấy tại https://aistudio.google.com/ . Không gửi khóa trong chat hoặc đưa vào mã nguồn.

## Phát triển và build

Yêu cầu Python 3.12 trên Windows. Cài thư viện trong [requirements.txt](requirements.txt), chạy [main.py](main.py). Các tác vụ VS Code được cung cấp để kiểm thử và build.

Lệnh tương đương trong môi trường Python đã chọn:

```powershell
python -m pip install -r requirements.txt
python -m unittest test_app -v
python -m PyInstaller --noconfirm --windowed --onedir --name KhanhToanStudio --collect-all imageio_ffmpeg main.py
```

Kiểm thử tự động bao gồm đọc CSV/Excel tiếng Việt, thiếu giá, token sai trang, trình tự đăng ảnh và tạo/đọc MP4 thật. Facebook/Gemini cần kiểm tra bằng tài khoản thật; bản build chưa chứng minh các API này hoạt động với tài khoản của bạn.
