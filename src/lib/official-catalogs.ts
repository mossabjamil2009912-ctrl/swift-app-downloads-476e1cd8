// الكتالوجات الرسمية الأصلية للمصنّع (بدون أي هوية لأكتس) — بدون تظليل.
// النسخة العربية مترجمة هندسياً بنفس تصميم ملف المصنّع مع إبقاء الرموز الفنية بالإنجليزية.
import type { Product } from "./products-data";

export function officialCatalogUrl(product: Product, lang: "en" | "ar"): string | null {
  const src = product.files.find((f) => f.kind === "Datasheet" || f.kind === "Catalog")?.url;
  if (!src) return null;
  if (lang === "en") return src;
  return `/catalogs/official-ar/${src.split("/").pop()}`;
}
