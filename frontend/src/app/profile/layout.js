export default function ProfileLayout({ children }) {
  return (
    <section>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #eee' }}>
        <strong>Profile Settings</strong>
      </nav>
      {children}
    </section>
  );
}
