import styles from "./Layouts.module.css";

export default function AuthLayout({ children }) {
  return (
    <div className={styles.authLayout}>
      {children}
    </div>
  );
}
