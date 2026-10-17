export type Gender = 'Men' | 'Women' | 'Kids';
export type ProductCategory =
  | 'Shirts'
  | 'T-Shirts'
  | 'Jeans'
  | 'Dresses'
  | 'Jackets'
  | 'Hoodies'
  | 'Ethnic Wear'
  | 'Footwear';

export type Product = {
  id: string;
  name: string;
  slug: string;
  gender: Gender;
  category: ProductCategory;
  price: number;
  originalPrice: number;
  rating: number;
  image: string;
  gallery: string[];
  colors: string[];
  sizes: string[];
  description: string;
  badge?: string;
};

export type CartItem = {
  id: string;
  name: string;
  image: string;
  price: number;
  size: string;
  color: string;
  quantity: number;
};
