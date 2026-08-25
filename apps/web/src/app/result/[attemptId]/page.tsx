"use client";

import { useParams } from "next/navigation";


export default function ResultPage() {
  const params = useParams<{ attemptId: string }>();

  return (
    <main className="content-page content-page--narrow">
      <section className="page-intro">
        <p className="eyebrow">Attempt {params.attemptId.slice(0, 8)}</p>
        <h1>Kết quả sẽ xuất hiện ở đây</h1>
        <p>Transcript và analysis được bổ sung sau recording và ASR.</p>
      </section>
    </main>
  );
}
