import Link from "next/link";


export function AppHeader() {
  return (
    <header className="site-header">
      <Link className="brand" href="/" aria-label="Clarivo home">
        <span className="brand-mark" aria-hidden="true">
          C
        </span>
        <span>Clarivo</span>
      </Link>
      <nav className="site-nav" aria-label="Điều hướng chính">
        <Link href="/practice">Luyện tập</Link>
        <Link href="/progress">Tiến bộ</Link>
      </nav>
    </header>
  );
}
