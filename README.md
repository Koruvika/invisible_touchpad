# INVISIBLE TOUCHPAD

## 1. Graphics UI
[Customtkinter](https://customtkinter.tomschimansky.com/documentation/) là thư viện được sử dụng chính trong quá trình 
xây dựng UI.

## 2. Main Functions
`Cursor Move`: Di chuyển con trỏ chuột ([pynput](https://pypi.org/project/pynput/))

`Scroll Screen`: Lướt màn hình

`Volume Controller`: tăng giảm âm lượng máy tính ([pycaw](https://github.com/AndreMiras/pycaw))

`Brightness Controller`: tăng giảm độ sáng màn hình ([screen-brightness-control](https://pypi.org/project/screen-brightness-control/))

## 3. UDP Communication
Giao tiếp từ xa thông qua giao thức UDP (socket)


# To-do List
- [ ] Bổ sung nội dung cho các combobox, hoặc thay đổi design
- [ ] Bổ sung Volume, Light Controller vào App
- [ ] Bổ sung (hoặc loại bỏ) Custom Cursor
- [ ] Kiểm thử
  - [ ] Đa luồng lúc đọc dữ liệu từ UDP
  - [ ] Các tính năng Volume, Light Controller
  - [ ] Các tham số DPI, Scroll Speed
  - [ ] 