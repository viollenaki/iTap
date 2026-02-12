import { doc, setDoc, serverTimestamp } from "firebase/firestore";
import { db } from "@/lib/firebase";

export const saveUserProfile = async (user) => {
  const providerId = user.providerData?.[0]?.providerId || "password";

  await setDoc(
    doc(db, "users", user.uid),
    {
      uid: user.uid,
      email: user.email || "",
      displayName: user.displayName || "",
      photoURL: user.photoURL || "",
      providerId,
      createdAt: user.metadata?.creationTime || null,
      lastLoginAt: serverTimestamp(),
    },
    { merge: true }
  );
};
