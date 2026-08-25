import Link from "next/link";


const principles = [
  {
    number: "01",
    title: "Nói điều chính trước",
    copy: "Tập trung vào câu trả lời cốt lõi trước khi thêm bối cảnh và chi tiết.",
  },
  {
    number: "02",
    title: "Một ý, một bằng chứng",
    copy: "Biến suy nghĩ trừu tượng thành lý do, ví dụ và kết quả cụ thể.",
  },
  {
    number: "03",
    title: "Thử lại có mục tiêu",
    copy: "Mỗi lần nói lại chỉ sửa những điểm có tác động lớn nhất đến người nghe.",
  },
];


export default function Home() {
  return (
    <main>
      <section className="hero">
        <div className="hero__content">
          <p className="eyebrow">Trợ lý luyện diễn đạt · Tiếng Việt</p>
          <h1>
            Nói rõ điều
            <br />
            <em>bạn thực sự nghĩ.</em>
          </h1>
          <p className="hero__lead">
            Clarivo giúp bạn biến một ý còn lộn xộn thành câu trả lời rõ ràng,
            ngắn gọn và dễ theo dõi — rồi thử lại ngay khi ý còn nóng.
          </p>
          <div className="hero__actions">
            <Link className="button button--primary" href="/practice">
              Bắt đầu luyện tập <span aria-hidden="true">→</span>
            </Link>
            <span className="hero__note">15 giây chuẩn bị · 60 giây nói</span>
          </div>
        </div>
        <div className="hero__visual" aria-label="Một lượt luyện tập cùng Clarivo">
          <div className="loop-card loop-card--prompt">
            <span>Câu hỏi luyện tập</span>
            <strong>“Hãy giải thích dự án gần nhất của bạn.”</strong>
          </div>
          <div className="voice-line" aria-hidden="true">
            {Array.from({ length: 22 }).map((_, index) => (
              <i key={index} />
            ))}
          </div>
          <div className="loop-card loop-card--feedback">
            <span>Điểm cần sửa trước</span>
            <strong>Ý chính xuất hiện quá muộn</strong>
            <small>Mở đầu trực tiếp bằng tên và mục tiêu của dự án.</small>
          </div>
          <div className="retry-pill">Nói lại · rõ hơn mỗi lần</div>
        </div>
      </section>

      <section className="principles" aria-labelledby="principles-title">
        <div className="section-heading">
          <p className="eyebrow">Cách Clarivo luyện cùng bạn</p>
          <h2 id="principles-title">Ít lời khuyên hơn. Đúng điểm hơn.</h2>
        </div>
        <div className="principle-grid">
          {principles.map((principle) => (
            <article key={principle.number}>
              <span>{principle.number}</span>
              <h3>{principle.title}</h3>
              <p>{principle.copy}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
