import Link from "next/link";
import styles from "./LandingHero.module.css";

export const LandingHero = () => {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <div className={styles.badge}>iTap beta</div>
        <div className={styles.hero}>
          <h1>Tap in. Stay synced. Shop smarter.</h1>
          <p>
            Create a quick account or sign in to keep your products, favorites,
            and alerts in one place.
          </p>
        </div>
        <div className={styles.actions}>
          <Link className={styles.primary} href="/sign-in">
            Sign in
          </Link>
          <Link className={styles.secondary} href="/sign-up">
            Create account
          </Link>
        </div>
      </main>
      <aside className={styles.panel}>
        <div className={styles.glow} />
        <div className={styles.panelContent}>
          <h2>Lightning fast checkouts</h2>
          <p>
            Save products, follow restocks, and get ready to tap whenever you
            shop.
          </p>
        </div>
      </aside>
    </div>
  );
};
