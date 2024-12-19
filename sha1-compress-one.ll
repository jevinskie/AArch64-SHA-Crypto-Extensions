; ModuleID = 'sha1-compress-one_extract.bc'
source_filename = "sha1-arm-unrolled.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "arm64-apple-macosx14.0.0"

%struct.CoolSHA1Digest = type { <4 x i32>, i32 }

; Function Attrs: mustprogress nofree noinline nosync nounwind ssp willreturn memory(argmem: write)
define void @sha1_arm_unrolled_compress_one(ptr noalias nocapture writeonly sret(%struct.CoolSHA1Digest) align 16 %0, <4 x i32> noundef %1, i32 noundef %2, [4 x <4 x i32>] %3) local_unnamed_addr #0 {
  %5 = extractvalue [4 x <4 x i32>] %3, 0
  %6 = extractvalue [4 x <4 x i32>] %3, 1
  %7 = extractvalue [4 x <4 x i32>] %3, 2
  %8 = extractvalue [4 x <4 x i32>] %3, 3
  %9 = bitcast <4 x i32> %5 to <16 x i8>
  %10 = shufflevector <16 x i8> %9, <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %11 = bitcast <16 x i8> %10 to <4 x i32>
  %12 = bitcast <4 x i32> %6 to <16 x i8>
  %13 = shufflevector <16 x i8> %12, <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %14 = bitcast <16 x i8> %13 to <4 x i32>
  %15 = bitcast <4 x i32> %7 to <16 x i8>
  %16 = shufflevector <16 x i8> %15, <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %17 = bitcast <16 x i8> %16 to <4 x i32>
  %18 = bitcast <4 x i32> %8 to <16 x i8>
  %19 = shufflevector <16 x i8> %18, <16 x i8> poison, <16 x i32> <i32 3, i32 2, i32 1, i32 0, i32 7, i32 6, i32 5, i32 4, i32 11, i32 10, i32 9, i32 8, i32 15, i32 14, i32 13, i32 12>
  %20 = bitcast <16 x i8> %19 to <4 x i32>
  %21 = add <4 x i32> %11, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %22 = add <4 x i32> %14, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %23 = extractelement <4 x i32> %1, i64 0
  %24 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %23)
  %25 = tail call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %1, i32 %2, <4 x i32> %21)
  %26 = add <4 x i32> %17, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %27 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %11, <4 x i32> %14, <4 x i32> %17)
  %28 = extractelement <4 x i32> %25, i64 0
  %29 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %28)
  %30 = tail call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %25, i32 %24, <4 x i32> %22)
  %31 = add <4 x i32> %20, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %32 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %27, <4 x i32> %20)
  %33 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %14, <4 x i32> %17, <4 x i32> %20)
  %34 = extractelement <4 x i32> %30, i64 0
  %35 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %34)
  %36 = tail call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %30, i32 %29, <4 x i32> %26)
  %37 = add <4 x i32> %32, <i32 1518500249, i32 1518500249, i32 1518500249, i32 1518500249>
  %38 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %33, <4 x i32> %32)
  %39 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %17, <4 x i32> %20, <4 x i32> %32)
  %40 = extractelement <4 x i32> %36, i64 0
  %41 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %40)
  %42 = tail call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %36, i32 %35, <4 x i32> %31)
  %43 = add <4 x i32> %38, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %44 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %39, <4 x i32> %38)
  %45 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %20, <4 x i32> %32, <4 x i32> %38)
  %46 = extractelement <4 x i32> %42, i64 0
  %47 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %46)
  %48 = tail call <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32> %42, i32 %41, <4 x i32> %37)
  %49 = add <4 x i32> %44, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %50 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %45, <4 x i32> %44)
  %51 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %32, <4 x i32> %38, <4 x i32> %44)
  %52 = extractelement <4 x i32> %48, i64 0
  %53 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %52)
  %54 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %48, i32 %47, <4 x i32> %43)
  %55 = add <4 x i32> %50, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %56 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %51, <4 x i32> %50)
  %57 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %38, <4 x i32> %44, <4 x i32> %50)
  %58 = extractelement <4 x i32> %54, i64 0
  %59 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %58)
  %60 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %54, i32 %53, <4 x i32> %49)
  %61 = add <4 x i32> %56, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %62 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %57, <4 x i32> %56)
  %63 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %44, <4 x i32> %50, <4 x i32> %56)
  %64 = extractelement <4 x i32> %60, i64 0
  %65 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %64)
  %66 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %60, i32 %59, <4 x i32> %55)
  %67 = add <4 x i32> %62, <i32 1859775393, i32 1859775393, i32 1859775393, i32 1859775393>
  %68 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %63, <4 x i32> %62)
  %69 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %50, <4 x i32> %56, <4 x i32> %62)
  %70 = extractelement <4 x i32> %66, i64 0
  %71 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %70)
  %72 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %66, i32 %65, <4 x i32> %61)
  %73 = add <4 x i32> %68, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %74 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %69, <4 x i32> %68)
  %75 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %56, <4 x i32> %62, <4 x i32> %68)
  %76 = extractelement <4 x i32> %72, i64 0
  %77 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %76)
  %78 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %72, i32 %71, <4 x i32> %67)
  %79 = add <4 x i32> %74, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %80 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %75, <4 x i32> %74)
  %81 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %62, <4 x i32> %68, <4 x i32> %74)
  %82 = extractelement <4 x i32> %78, i64 0
  %83 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %82)
  %84 = tail call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %78, i32 %77, <4 x i32> %73)
  %85 = add <4 x i32> %80, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %86 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %81, <4 x i32> %80)
  %87 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %68, <4 x i32> %74, <4 x i32> %80)
  %88 = extractelement <4 x i32> %84, i64 0
  %89 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %88)
  %90 = tail call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %84, i32 %83, <4 x i32> %79)
  %91 = add <4 x i32> %86, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %92 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %87, <4 x i32> %86)
  %93 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %74, <4 x i32> %80, <4 x i32> %86)
  %94 = extractelement <4 x i32> %90, i64 0
  %95 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %94)
  %96 = tail call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %90, i32 %89, <4 x i32> %85)
  %97 = add <4 x i32> %92, <i32 -1894007588, i32 -1894007588, i32 -1894007588, i32 -1894007588>
  %98 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %93, <4 x i32> %92)
  %99 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %80, <4 x i32> %86, <4 x i32> %92)
  %100 = extractelement <4 x i32> %96, i64 0
  %101 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %100)
  %102 = tail call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %96, i32 %95, <4 x i32> %91)
  %103 = add <4 x i32> %98, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %104 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %99, <4 x i32> %98)
  %105 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %86, <4 x i32> %92, <4 x i32> %98)
  %106 = extractelement <4 x i32> %102, i64 0
  %107 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %106)
  %108 = tail call <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32> %102, i32 %101, <4 x i32> %97)
  %109 = add <4 x i32> %104, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %110 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %105, <4 x i32> %104)
  %111 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %92, <4 x i32> %98, <4 x i32> %104)
  %112 = extractelement <4 x i32> %108, i64 0
  %113 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %112)
  %114 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %108, i32 %107, <4 x i32> %103)
  %115 = add <4 x i32> %110, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %116 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %111, <4 x i32> %110)
  %117 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32> %98, <4 x i32> %104, <4 x i32> %110)
  %118 = extractelement <4 x i32> %114, i64 0
  %119 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %118)
  %120 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %114, i32 %113, <4 x i32> %109)
  %121 = add <4 x i32> %116, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %122 = tail call <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32> %117, <4 x i32> %116)
  %123 = extractelement <4 x i32> %120, i64 0
  %124 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %123)
  %125 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %120, i32 %119, <4 x i32> %115)
  %126 = add <4 x i32> %122, <i32 -899497514, i32 -899497514, i32 -899497514, i32 -899497514>
  %127 = extractelement <4 x i32> %125, i64 0
  %128 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %127)
  %129 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %125, i32 %124, <4 x i32> %121)
  %130 = extractelement <4 x i32> %129, i64 0
  %131 = tail call i32 @llvm.aarch64.crypto.sha1h(i32 %130)
  %132 = tail call <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32> %129, i32 %128, <4 x i32> %126)
  %133 = add <4 x i32> %132, %1
  %134 = add i32 %131, %2
  store <4 x i32> %133, ptr %0, align 16, !tbaa !5
  %135 = getelementptr inbounds %struct.CoolSHA1Digest, ptr %0, i64 0, i32 1
  store i32 %134, ptr %135, align 16, !tbaa !8
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare i32 @llvm.aarch64.crypto.sha1h(i32) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1c(<4 x i32>, i32, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1su0(<4 x i32>, <4 x i32>, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1su1(<4 x i32>, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1p(<4 x i32>, i32, <4 x i32>) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(none)
declare <4 x i32> @llvm.aarch64.crypto.sha1m(<4 x i32>, i32, <4 x i32>) #1

attributes #0 = { mustprogress nofree noinline nosync nounwind ssp willreturn memory(argmem: write) "frame-pointer"="non-leaf" "min-legal-vector-width"="128" "no-trapping-math"="true" "probe-stack"="__chkstk_darwin" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+crypto,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+sm4,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(none) }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 2, !"SDK Version", [2 x i32] [i32 14, i32 5]}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 8, !"PIC Level", i32 2}
!3 = !{i32 7, !"frame-pointer", i32 1}
!4 = !{!"Apple clang version 15.0.0 (clang-1500.3.9.4)"}
!5 = !{!6, !6, i64 0}
!6 = !{!"omnipotent char", !7, i64 0}
!7 = !{!"Simple C++ TBAA"}
!8 = !{!9, !10, i64 16}
!9 = !{!"_ZTS14CoolSHA1Digest", !6, i64 0, !10, i64 16}
!10 = !{!"int", !6, i64 0}
